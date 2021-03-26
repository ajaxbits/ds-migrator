from dsmigrator.LIConfig import LIGet, LIDescribe, LICustom, LIReplace


def li_config_transform(allofpolicy, OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY):
    liruleid = LIGet(allofpolicy)

    alllirule, allliruleidnew1, allliruleidold, alllicustomrule = LIDescribe(
        liruleid, OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY
    )

    allliruleidnew2 = LICustom(alllirule, alllicustomrule, NEW_HOST, NEW_API_KEY)

    aop_replace_li_rules = LIReplace(
        allofpolicy,
        allliruleidnew1,
        allliruleidnew2,
        liruleid,
        allliruleidold,
        alllicustomrule,
    )
    final = aop_replace_li_rules
    return final
