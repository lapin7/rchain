/* automatically generated by pepy 7.0 #14 (nanook.mcc.com), do not edit! */

#include "psap.h"

#define	advise	ryr_advise

void	advise ();

/* Generated from module PasswordLookup */

#include <stdio.h>
#include "PasswordLookup-types.h"

#ifndef PEPYPARM
#define PEPYPARM char *
#endif /* PEPYPARM */
extern PEPYPARM NullParm;

/* ARGSUSED */

int	encode_PasswordLookup_UserName (pe, explicit, len, buffer, parm)
register PE     *pe;
int	explicit;
int	len;
char   *buffer;
struct type_PasswordLookup_UserName * parm;
{
    if (encode_UNIV_GraphicString (pe, 0, len, buffer, parm ) == NOTOK)
        return NOTOK;
    (*pe) -> pe_class = PE_CLASS_APPL;
    (*pe) -> pe_id = 2;

#ifdef DEBUG
    (void) testdebug ((*pe), "PasswordLookup.UserName");
#endif


    return OK;
}
