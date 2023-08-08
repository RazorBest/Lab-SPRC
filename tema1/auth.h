/*
 * Please do not edit this file.
 * It was generated using rpcgen.
 */

#ifndef _AUTH_H_RPCGEN
#define _AUTH_H_RPCGEN

#include <rpc/rpc.h>


#ifdef __cplusplus
extern "C" {
#endif


enum status_code {
	S_UNKNOWN = 0,
	S_SUCCESS = 4,
	S_USER_NOT_FOUND = 8,
	S_REQUEST_DENIED = 16,
	S_PERMISSION_DENIED = 17,
	S_TOKEN_EXPIRED = 18,
	S_RESOURCE_NOT_FOUND = 19,
	S_OPERATION_NOT_PERMITTED = 20,
	S_PERMISSION_GRANTED = 21,
};
typedef enum status_code status_code;

enum Operation {
	REQUEST = 2,
	READ = 4,
	INSERT = 8,
	MODIFY = 16,
	DELETE = 32,
	EXECUTE = 64,
	INTERCONTINENTAL_BALLISTIC_MISSILE = 128,
};
typedef enum Operation Operation;

struct auth_output {
	status_code status;
	char auth_token[16];
};
typedef struct auth_output auth_output;

struct access_input {
	char id[16];
	char auth_token[16];
	char *permissions;
	u_char signature[64];
	int regen;
};
typedef struct access_input access_input;

struct access_output {
	status_code status;
	char access_token[16];
	char regen_token[16];
	int life;
};
typedef struct access_output access_output;

struct approve_input {
	char id[16];
	char auth_token[16];
};
typedef struct approve_input approve_input;

struct approve_output {
	status_code status;
	char auth_token[16];
	char *permissions;
	u_char signature[64];
};
typedef struct approve_output approve_output;

struct validate_input {
	Operation operation;
	char access_token[16];
	char *resource;
};
typedef struct validate_input validate_input;

#define REQUESTAUTH_PROG 0x31234077
#define REQUESTAUTH_VERS 1

#if defined(__STDC__) || defined(__cplusplus)
#define REQUESTAUTH 1
extern  auth_output * requestauth_1(char **, CLIENT *);
extern  auth_output * requestauth_1_svc(char **, struct svc_req *);
#define REQUESTACCESS 2
extern  access_output * requestaccess_1(access_input *, CLIENT *);
extern  access_output * requestaccess_1_svc(access_input *, struct svc_req *);
#define APPROVETOKEN 3
extern  approve_output * approvetoken_1(approve_input *, CLIENT *);
extern  approve_output * approvetoken_1_svc(approve_input *, struct svc_req *);
#define VALIDATEACTION 4
extern  status_code * validateaction_1(validate_input *, CLIENT *);
extern  status_code * validateaction_1_svc(validate_input *, struct svc_req *);
extern int requestauth_prog_1_freeresult (SVCXPRT *, xdrproc_t, caddr_t);

#else /* K&R C */
#define REQUESTAUTH 1
extern  auth_output * requestauth_1();
extern  auth_output * requestauth_1_svc();
#define REQUESTACCESS 2
extern  access_output * requestaccess_1();
extern  access_output * requestaccess_1_svc();
#define APPROVETOKEN 3
extern  approve_output * approvetoken_1();
extern  approve_output * approvetoken_1_svc();
#define VALIDATEACTION 4
extern  status_code * validateaction_1();
extern  status_code * validateaction_1_svc();
extern int requestauth_prog_1_freeresult ();
#endif /* K&R C */

/* the xdr functions */

#if defined(__STDC__) || defined(__cplusplus)
extern  bool_t xdr_status_code (XDR *, status_code*);
extern  bool_t xdr_Operation (XDR *, Operation*);
extern  bool_t xdr_auth_output (XDR *, auth_output*);
extern  bool_t xdr_access_input (XDR *, access_input*);
extern  bool_t xdr_access_output (XDR *, access_output*);
extern  bool_t xdr_approve_input (XDR *, approve_input*);
extern  bool_t xdr_approve_output (XDR *, approve_output*);
extern  bool_t xdr_validate_input (XDR *, validate_input*);

#else /* K&R C */
extern bool_t xdr_status_code ();
extern bool_t xdr_Operation ();
extern bool_t xdr_auth_output ();
extern bool_t xdr_access_input ();
extern bool_t xdr_access_output ();
extern bool_t xdr_approve_input ();
extern bool_t xdr_approve_output ();
extern bool_t xdr_validate_input ();

#endif /* K&R C */

#ifdef __cplusplus
}
#endif

#endif /* !_AUTH_H_RPCGEN */
