from functions.IMConfig import IMGet, IMDescribe, IMCustom, IMReplace


def im_config_transform(allofpolicy, OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY):
    imruleid = IMGet(allofpolicy)

    allimrule, allimruleidnew1, allimruleidold, allimcustomrule = IMDescribe(
        imruleid, OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY
    )

    allimruleidnew2 = IMCustom(allimrule, allimcustomrule, NEW_HOST, NEW_API_KEY)
    aop_replace_im_rules = IMReplace(
        allofpolicy,
        allimruleidnew1,
        allimruleidnew2,
        imruleid,
        allimruleidold,
        allimcustomrule,
    )
    final = aop_replace_im_rules
    return final
