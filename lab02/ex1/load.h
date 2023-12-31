/*
 * Please do not edit this file.
 * It was generated using rpcgen.
 */

#ifndef _LOAD_H_RPCGEN
#define _LOAD_H_RPCGEN

#include <rpc/rpc.h>


#ifdef __cplusplus
extern "C" {
#endif


struct numbers {
	int a;
	int b;
};
typedef struct numbers numbers;

#define LOAD_PROG 222222222
#define LOAD_VERS 1

#if defined(__STDC__) || defined(__cplusplus)
#define SUM 1
extern  int * sum_1(numbers *, CLIENT *);
extern  int * sum_1_svc(numbers *, struct svc_req *);
extern int load_prog_1_freeresult (SVCXPRT *, xdrproc_t, caddr_t);

#else /* K&R C */
#define SUM 1
extern  int * sum_1();
extern  int * sum_1_svc();
extern int load_prog_1_freeresult ();
#endif /* K&R C */

/* the xdr functions */

#if defined(__STDC__) || defined(__cplusplus)
extern  bool_t xdr_numbers (XDR *, numbers*);

#else /* K&R C */
extern bool_t xdr_numbers ();

#endif /* K&R C */

#ifdef __cplusplus
}
#endif

#endif /* !_LOAD_H_RPCGEN */
