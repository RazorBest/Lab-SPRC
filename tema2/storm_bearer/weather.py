import argparse
import asyncio
import functools
import logging
import os
import tornado.web
import psycopg2
import time
import json
import jsonschema

DATABASE = None

def verify_body_json(error_code, stop=True):
    """
    Decorator used for a tornado request handler.
    Checks if the response body is a valid JSON.
    Sets a status error code, if the JSON verification fails.
    If the verification fails, by default, the flow stops, and the decorated
    function won't be called.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            data = {}
            try:
                data = json.loads(self.request.body)
            except json.JSONDecodeError:
                logging.debug("JSON fail")
                self.set_status(error_code)
                if stop:
                    return

            kwargs['data'] = data
            func(self, *args, **kwargs)

        return wrapper
    return decorator

def validate_input_schema(input_schema, error_code, stop=True):
    """
    Decorator used for a tornado request handler.
    The decorated function must have a keyword argument named `data`.
    Checks if the data keyword argument has the specified input schema.
    Sets a status error code, if the schema verification fails.
    If the verification fails, by default, the flow stops, and the decorated
    function won't be called.
    """
    jsonschema.validators.Draft201909Validator.check_schema(input_schema)

    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, data=None, **kwargs):
            logging.debug(data)
            logging.debug(input_schema)
            try:
                jsonschema.validate(data, input_schema)
            except jsonschema.ValidationError:
                logging.debug("Input schema fail")
                self.set_status(error_code)
                if stop:
                    return

            func(self, *args, data, **kwargs)

        return wrapper
    return decorator


class CountryAllHandler(tornado.web.RequestHandler):
    def get(self):
        with DATABASE:
            with DATABASE.cursor() as curs:
                sql = "SELECT id, name, latitude, longitude FROM countries LIMIT 100000;"
                try:
                    curs.execute(sql)
                except Exception as exc:
                    logging.exception(exc)
                    self.finish(json.dumps([]))
                    return
                
                output = []
                for record in curs:
                    country = {"id": record[0], "nume": record[1], "lat": record[2], "lon": record[3]}
                    output.append(country)

                self.finish(json.dumps(output))

    @verify_body_json(400)
    @validate_input_schema({
        "type": "object",
        "properties": {
            "nume": {"type": "string"},
            "lat": {"type": "number"},
            "lon": {"type": "number"},
        },
        "required": ["nume", "lat", "lon"],
    }, 400)
    def post(self, data=None):
        logging.debug(data)
        name = data["nume"]
        lat = data["lat"]
        lon = data["lon"]
        
        with DATABASE:
            with DATABASE.cursor() as curs:
                sql = "INSERT INTO countries (id, name, latitude, longitude) \
                        VALUES (DEFAULT, %s, %s, %s)\
                        RETURNING id;"
                data = (name, lat, lon)
                # Always let psycopg2 do the interpolation
                # It will prevent injection vulnerabilities 
                try:
                    curs.execute(sql, data)
                except psycopg2.errors.UniqueViolation:
                    self.set_status(409)
                    return
                except Exception as exc:
                    logging.exception(exc)
                    self.set_status(400)
                    return

                record = curs.fetchone()

                if type(record) != tuple or len(record) != 1:
                    self.set_status(400)
                    logging.warning("Unhandled return format after sql query")
                    return

                country_id = record[0]

                self.set_status(201)
                self.finish(json.dumps({"id": country_id}))

class CountryIdHandler(tornado.web.RequestHandler):
    @verify_body_json(400)
    @validate_input_schema({
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "nume": {"type": "string"},
            "lat": {"type": "number"},
            "lon": {"type": "number"},
        },
        "required": ["id", "nume", "lat", "lon"],
    }, 400)
    def put(self, country_id, data=None):
        country_id = int(country_id)
        if data["id"] != country_id:
            self.set_status(400)
            return

        name = data["nume"]
        lat = data["lat"]
        lon = data["lon"]

        with DATABASE:
            with DATABASE.cursor() as curs:
                sql = "UPDATE countries \
                        SET name = %s, \
                            latitude = %s, \
                            longitude = %s \
                        WHERE id = %s \
                        RETURNING id"
                data = (name, lat, lon, country_id)
                # Always let psycopg2 do the interpolation
                # It will prevent injection vulnerabilities 
                try:
                    curs.execute(sql, data)
                except psycopg2.errors.UniqueViolation:
                    self.set_status(400)
                    return
                except Exception as exc:
                    logging.exception(exc)
                    self.set_status(400)
                    return

                records = list(curs)
                if len(records) != 1:
                    self.set_status(404)
                    return

                self.set_status(200)

    def delete(self, country_id):
        with DATABASE:
            with DATABASE.cursor() as curs:
                sql = "DELETE FROM countries \
                        WHERE id = %s \
                        RETURNING id"
                data = (country_id,)
                # Always let psycopg2 do the interpolation
                # It will prevent injection vulnerabilities 
                try:
                    curs.execute(sql, data)
                except Exception as exc:
                    logging.exception(exc)
                    self.set_status(400)
                    return

                records = list(curs)
                if len(records) > 1:
                    logging.error("More than one entry was deleted")
                    logging.error(records)

                if len(records) != 1:
                    self.set_status(404)
                    return

                self.set_status(200)
        

class CityAllHandler(tornado.web.RequestHandler):
    def get(self):
        with DATABASE:
            with DATABASE.cursor() as curs:
                sql = "SELECT id, country_id, name, latitude, longitude FROM cities LIMIT 100000;"
                try:
                    curs.execute(sql)
                except Exception as exc:
                    logging.exception(exc)
                    self.finish(json.dumps([]))
                    return
                
                output = []
                for record in curs:
                    country = {"id": record[0], "idTara": record[1], 
                        "nume": record[2], "lat": record[3], "lon": record[4]
                    }
                    output.append(country)

                self.finish(json.dumps(output))

    @verify_body_json(400)
    @validate_input_schema({
        "type": "object",
        "properties": {
            "idTara": {"type": "integer"},
            "nume": {"type": "string"},
            "lat": {"type": "number"},
            "lon": {"type": "number"},
        },
        "required": ["idTara", "nume", "lat", "lon"],
    }, 400)
    def post(self, data=None):
        country_id = data["idTara"]
        name = data["nume"]
        lat = data["lat"]
        lon = data["lon"]
        
        with DATABASE:
            with DATABASE.cursor() as curs:
                sql = "INSERT INTO cities (id, country_id, name, latitude, longitude) \
                        VALUES (DEFAULT, %s, %s, %s, %s)\
                        RETURNING id;"
                data = (country_id, name, lat, lon)
                # Always let psycopg2 do the interpolation
                # It will prevent injection vulnerabilities 
                try:
                    curs.execute(sql, data)
                except (psycopg2.errors.UniqueViolation, psycopg2.errors.ForeignKeyViolation):
                    self.set_status(409)
                    return
                except Exception as exc:
                    logging.exception(exc)
                    self.set_status(400)
                    return

                record = curs.fetchone()

                if type(record) != tuple or len(record) != 1:
                    self.set_status(400)
                    logging.warning("Unhandled return format after sql query")
                    return

                city_id = record[0]
                
                self.set_status(201)
                self.finish(json.dumps({"id": city_id}))

class CityCountryIdHandler(tornado.web.RequestHandler):
    def get(self, country_id):
        with DATABASE:
            with DATABASE.cursor() as curs:
                sql = "SELECT id, country_id, name, latitude, longitude FROM cities \
                        WHERE country_id = %s \
                        LIMIT 100000;"
                data = (country_id,)
                # Always let psycopg2 do the interpolation
                # It will prevent injection vulnerabilities 
                try:
                    curs.execute(sql, data)
                except Exception as exc:
                    logging.exception(exc)
                    self.finish(json.dumps([]))
                    return
                
                output = []
                for record in curs:
                    country = {"id": record[0], "idTara": record[1], 
                        "nume": record[2], "lat": record[3], "lon": record[4]
                    }
                    output.append(country)

                self.finish(json.dumps(output))

class CityIdHandler(tornado.web.RequestHandler):
    @verify_body_json(400)
    @validate_input_schema({
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "idTara": {"type": "integer"},
            "nume": {"type": "string"},
            "lat": {"type": "number"},
            "lon": {"type": "number"},
        },
        "required": ["id", "idTara", "nume", "lat", "lon"],
    }, 400)
    def put(self, city_id, data=None):
        city_id = int(city_id)
        if data["id"] != city_id:
            self.set_status(400)
            return

        country_id = data["idTara"]
        name = data["nume"]
        lat = data["lat"]
        lon = data["lon"]
        
        with DATABASE:
            with DATABASE.cursor() as curs:
                sql = "UPDATE cities \
                        SET country_id = %s, \
                            name = %s, \
                            latitude = %s, \
                            longitude = %s \
                        WHERE id = %s \
                        RETURNING id"
                data = (country_id, name, lat, lon, city_id)
                # Always let psycopg2 do the interpolation
                # It will prevent injection vulnerabilities 
                try:
                    curs.execute(sql, data)
                except (psycopg2.errors.UniqueViolation, psycopg2.errors.ForeignKeyViolation):
                    self.set_status(409)
                    return
                except Exception as exc:
                    logging.exception(exc)
                    self.set_status(400)
                    return

                records = list(curs)
                if len(records) != 1:
                    self.set_status(404)
                    return

                self.set_status(200)

    def delete(self, city_id):
        with DATABASE:
            with DATABASE.cursor() as curs:
                sql = "DELETE FROM cities \
                        WHERE id = %s \
                        RETURNING id"
                data = (city_id,)
                # Always let psycopg2 do the interpolation
                # It will prevent injection vulnerabilities 
                try:
                    curs.execute(sql, data)
                except Exception as exc:
                    logging.exception(exc)
                    self.set_status(400)
                    return

                records = list(curs)
                if len(records) > 1:
                    logging.error("More than one entry was deleted")
                    logging.error(records)

                if len(records) != 1:
                    self.set_status(404)
                    return

                self.set_status(200)


class TemperatureAllHandler(tornado.web.RequestHandler):
    def get(self):
        lat = self.get_argument("lat", None)
        lon = self.get_argument("lon", None)
        from_time = self.get_argument("from", "4713-01-01 00:00 BC")
        until_time = self.get_argument("until", "294275-01-01 00:00 AD")

        if lat is not None:
            try:
                lat = float(lat)
            except ValueError:
                self.finish(json.dumps([]))
                return

        if lon is not None:
            try:
                lon = float(lon)
            except ValueError:
                self.finish(json.dumps([]))
                return

        with DATABASE:
            with DATABASE.cursor() as curs:
                sql = "SELECT t1.id, t1.value, t1.timestamp FROM temperatures t1 \
                        JOIN cities t2 ON t1.city_id = t2.id \
                        WHERE timestamp BETWEEN %(from)s AND %(until)s \
                            AND (%(lat)s IS NULL OR t2.latitude = %(lat)s) \
                            AND (%(lon)s IS NULL OR t2.longitude = %(lon)s) \
                        LIMIT 100000;"
                data = {"from": from_time, "until": until_time, "lat": lat, "lon": lon}
                # Always let psycopg2 do the interpolation
                # It will prevent injection vulnerabilities 
                try:
                    curs.execute(sql, data)
                except Exception as exc:
                    logging.exception(exc)
                    self.finish(json.dumps([]))
                    return
                
                output = []
                for record in curs:
                    country = {"id": record[0], "valoare": record[1],
                        "timestamp": record[2].strftime('%Y-%m-%d')}
                    output.append(country)

                self.finish(json.dumps(output))

    @verify_body_json(400)
    @validate_input_schema({
        "type": "object",
        "properties": {
            "idOras": {"type": "integer"},
            "valoare": {"type": "number"},
        },
        "required": ["idOras", "valoare"],
    }, 400)
    def post(self, data=None):
        city_id = data["idOras"]
        temp_value = data["valoare"]
        
        with DATABASE:
            with DATABASE.cursor() as curs:
                sql = "INSERT INTO temperatures (id, timestamp, value, city_id)  \
                        VALUES (DEFAULT, NOW(), %s, %s) \
                        RETURNING id;"
                data = (temp_value, city_id)
                # Always let psycopg2 do the interpolation
                # It will prevent injection vulnerabilities 
                try:
                    curs.execute(sql, data)
                except (psycopg2.errors.UniqueViolation, psycopg2.errors.ForeignKeyViolation):
                    self.set_status(409)
                    return
                except Exception as exc:
                    logging.exception(exc)
                    self.set_status(400)
                    return

                record = curs.fetchone()

                if type(record) != tuple or len(record) != 1:
                    self.set_status(400)
                    logging.warning("Unhandled return format after sql query")
                    return

                temperature_id = record[0]

                self.set_status(201)
                self.finish(json.dumps({"id": temperature_id}))

class TemperatureCityHandler(tornado.web.RequestHandler):
    def get(self, city_id):
        from_time = self.get_argument("from", "4713-01-01 00:00 BC")
        until_time = self.get_argument("until", "294275-01-01 00:00 AD")

        with DATABASE:
            with DATABASE.cursor() as curs:
                sql = "SELECT t1.id, t1.value, t1.timestamp FROM temperatures t1 \
                        WHERE timestamp BETWEEN %(from)s AND %(until)s \
                            AND city_id = %(city_id)s \
                        LIMIT 100000;"
                data = {"city_id": city_id, "from": from_time, "until": until_time}
                # Always let psycopg2 do the interpolation
                # It will prevent injection vulnerabilities 
                try:
                    curs.execute(sql, data)
                except Exception as exc:
                    logging.exception(exc)
                    self.finish(json.dumps([]))
                    return
                
                output = []
                for record in curs:
                    country = {"id": record[0], "valoare": record[1],
                        "timestamp": record[2].strftime("%Y-%m-%d")}
                    output.append(country)

                self.finish(json.dumps(output))

class TemperatureCountryHandler(tornado.web.RequestHandler):
    def get(self, country_id):
        from_time = self.get_argument("from", "4713-01-01 00:00 BC")
        until_time = self.get_argument("until", "294275-01-01 00:00 AD")

        with DATABASE:
            with DATABASE.cursor() as curs:
                sql = "SELECT t1.id, t1.value, t1.timestamp FROM temperatures t1 \
                        JOIN cities t2 ON t2.id = t1.city_id \
                        JOIN countries t3 ON t3.id = t2.country_id \
                        WHERE timestamp BETWEEN %(from)s AND %(until)s \
                            AND t3.id = %(country_id)s \
                        LIMIT 100000;"
                data = {"country_id": country_id, "from": from_time, "until": until_time}
                # Always let psycopg2 do the interpolation
                # It will prevent injection vulnerabilities 
                try:
                    curs.execute(sql, data)
                except Exception as exc:
                    logging.exception(exc)
                    self.finish(json.dumps([]))
                    return
                
                output = []
                for record in curs:
                    country = {"id": record[0], "valoare": record[1],
                        "timestamp": record[2].strftime("%Y-%m-%d")}
                    output.append(country)

                self.finish(json.dumps(output))

class TemperatureIdHandler(tornado.web.RequestHandler):
    @verify_body_json(400)
    @validate_input_schema({
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "idOras": {"type": "integer"},
            "valoare": {"type": "number"},
        },
        "required": ["id", "idOras", "valoare"],
    }, 400)
    def put(self, temperature_id, data=None):
        temperature_id = int(temperature_id)
        if data["id"] != temperature_id:
            self.set_status(400)
            return

        city_id = data["idOras"]
        value = data["valoare"]
        
        with DATABASE:
            with DATABASE.cursor() as curs:
                sql = "UPDATE temperatures \
                        SET city_id = %s, \
                            value = %s \
                        WHERE id = %s \
                        RETURNING id"
                data = (city_id, value, temperature_id)
                # Always let psycopg2 do the interpolation
                # It will prevent injection vulnerabilities 
                try:
                    curs.execute(sql, data)
                except psycopg2.errors.UniqueViolation:
                    self.set_status(400)
                    return
                except Exception as exc:
                    logging.exception(exc)
                    self.set_status(400)
                    return

                records = list(curs)
                if len(records) != 1:
                    self.set_status(404)
                    return

                self.set_status(200)

    def delete(self, temperature_id):
        with DATABASE:
            with DATABASE.cursor() as curs:
                sql = "DELETE FROM temperatures \
                        WHERE id = %s \
                        RETURNING id"
                data = (temperature_id,)
                # Always let psycopg2 do the interpolation
                # It will prevent injection vulnerabilities 
                try:
                    curs.execute(sql, data)
                except Exception as exc:
                    logging.exception(exc)
                    self.set_status(400)
                    return

                records = list(curs)
                if len(records) > 1:
                    logging.error("More than one entry was deleted")
                    logging.error(records)

                if len(records) != 1:
                    self.set_status(404)
                    return

                self.set_status(200)

def make_app():
    return tornado.web.Application([
        (r"/api/countries/?", CountryAllHandler),
        (r"/api/countries/([0-9]+)", CountryIdHandler),
        (r"/api/cities/?", CityAllHandler),
        (r"/api/cities/country/([0-9]+)", CityCountryIdHandler),
        (r"/api/cities/([0-9]+)", CityIdHandler),
        (r"/api/temperatures/?", TemperatureAllHandler),
        (r"/api/temperatures/cities/([0-9]+)", TemperatureCityHandler),
        (r"/api/temperatures/countries/([0-9]+)", TemperatureCountryHandler),
        (r"/api/temperatures/([0-9]+)", TemperatureIdHandler),
    ])

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", default=6000)

    args = parser.parse_args()

    return args

async def main():
    db_user = os.environ.get("POSTGRES_USER", None)
    db_password = os.environ.get("POSTGRES_PASSWORD", None)
    dbname = os.environ.get("POSTGRES_DB", None)
    dbhost = os.environ.get("DB_SERVICE_HOSTNAME", None)
    dbport = os.environ.get("DB_SERVICE_PORT", None)

    logging.debug("db_user: %s", db_user)
    logging.debug("dbname: %s", dbname)
    logging.debug("db host: %s", dbhost)
    logging.debug("db port: %s", dbport)

    # Get commandline arguments
    args = get_args()
    server_port = args.port

    if db_user is None or db_password is None or dbname is None \
            or dbhost is None or dbport is None:
        logging.error("Not all needed environment variables are set. Please check.")
        return

    app = make_app()
    app.listen(server_port)

    logging.info(f"Started server on port {server_port}")

    url = "db"

    time.sleep(4)

    global DATABASE
    DATABASE = psycopg2.connect(dbname=dbname, user=db_user,
        password=db_password, host=dbhost, port=dbport)

    await asyncio.Event().wait()

if __name__ == "__main__":
    logger = logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())
