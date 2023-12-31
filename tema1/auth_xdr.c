/*
 * Please do not edit this file.
 * It was generated using rpcgen.
 */

#include "auth.h"

bool_t
xdr_status_code (XDR *xdrs, status_code *objp)
{
	register int32_t *buf;

	 if (!xdr_enum (xdrs, (enum_t *) objp))
		 return FALSE;
	return TRUE;
}

bool_t
xdr_Operation (XDR *xdrs, Operation *objp)
{
	register int32_t *buf;

	 if (!xdr_enum (xdrs, (enum_t *) objp))
		 return FALSE;
	return TRUE;
}

bool_t
xdr_auth_output (XDR *xdrs, auth_output *objp)
{
	register int32_t *buf;

	int i;
	 if (!xdr_status_code (xdrs, &objp->status))
		 return FALSE;
	 if (!xdr_vector (xdrs, (char *)objp->auth_token, 16,
		sizeof (char), (xdrproc_t) xdr_char))
		 return FALSE;
	return TRUE;
}

bool_t
xdr_access_input (XDR *xdrs, access_input *objp)
{
	register int32_t *buf;

	int i;
	 if (!xdr_vector (xdrs, (char *)objp->id, 16,
		sizeof (char), (xdrproc_t) xdr_char))
		 return FALSE;
	 if (!xdr_vector (xdrs, (char *)objp->auth_token, 16,
		sizeof (char), (xdrproc_t) xdr_char))
		 return FALSE;
	 if (!xdr_string (xdrs, &objp->permissions, ~0))
		 return FALSE;
	 if (!xdr_vector (xdrs, (char *)objp->signature, 64,
		sizeof (u_char), (xdrproc_t) xdr_u_char))
		 return FALSE;
	 if (!xdr_int (xdrs, &objp->regen))
		 return FALSE;
	return TRUE;
}

bool_t
xdr_access_output (XDR *xdrs, access_output *objp)
{
	register int32_t *buf;

	int i;
	 if (!xdr_status_code (xdrs, &objp->status))
		 return FALSE;
	 if (!xdr_vector (xdrs, (char *)objp->access_token, 16,
		sizeof (char), (xdrproc_t) xdr_char))
		 return FALSE;
	 if (!xdr_vector (xdrs, (char *)objp->regen_token, 16,
		sizeof (char), (xdrproc_t) xdr_char))
		 return FALSE;
	 if (!xdr_int (xdrs, &objp->life))
		 return FALSE;
	return TRUE;
}

bool_t
xdr_approve_input (XDR *xdrs, approve_input *objp)
{
	register int32_t *buf;

	int i;
	 if (!xdr_vector (xdrs, (char *)objp->id, 16,
		sizeof (char), (xdrproc_t) xdr_char))
		 return FALSE;
	 if (!xdr_vector (xdrs, (char *)objp->auth_token, 16,
		sizeof (char), (xdrproc_t) xdr_char))
		 return FALSE;
	return TRUE;
}

bool_t
xdr_approve_output (XDR *xdrs, approve_output *objp)
{
	register int32_t *buf;

	int i;
	 if (!xdr_status_code (xdrs, &objp->status))
		 return FALSE;
	 if (!xdr_vector (xdrs, (char *)objp->auth_token, 16,
		sizeof (char), (xdrproc_t) xdr_char))
		 return FALSE;
	 if (!xdr_string (xdrs, &objp->permissions, ~0))
		 return FALSE;
	 if (!xdr_vector (xdrs, (char *)objp->signature, 64,
		sizeof (u_char), (xdrproc_t) xdr_u_char))
		 return FALSE;
	return TRUE;
}

bool_t
xdr_validate_input (XDR *xdrs, validate_input *objp)
{
	register int32_t *buf;

	int i;
	 if (!xdr_Operation (xdrs, &objp->operation))
		 return FALSE;
	 if (!xdr_vector (xdrs, (char *)objp->access_token, 16,
		sizeof (char), (xdrproc_t) xdr_char))
		 return FALSE;
	 if (!xdr_string (xdrs, &objp->resource, ~0))
		 return FALSE;
	return TRUE;
}
