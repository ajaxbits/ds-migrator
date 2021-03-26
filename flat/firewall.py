from functions.FirewallConfig import (
    FirewallGet,
    FirewallDescribe,
    FirewallCustom,
    FirewallReplace,
)


def firewall_config_transform(
    allofpolicy,
    t1iplistid,
    t2iplistid,
    t1maclistid,
    t2maclistid,
    t1portlistid,
    t2portlistid,
    t1statefulid,
    t2statefulid,
    OLD_HOST,
    OLD_API_KEY,
    NEW_HOST,
    NEW_API_KEY,
):
    firewallruleid, policystateful = FirewallGet(allofpolicy)
    (
        allfirewallrule,
        allfirewallruleidnew1,
        allfirewallruleidold,
        allfirewallcustomrule,
    ) = FirewallDescribe(
        firewallruleid,
        t1iplistid,
        t2iplistid,
        t1maclistid,
        t2maclistid,
        t1portlistid,
        t2portlistid,
        OLD_HOST,
        OLD_API_KEY,
        NEW_HOST,
        NEW_API_KEY,
    )
    allfirewallruleidnew2 = FirewallCustom(
        allfirewallrule, allfirewallcustomrule, NEW_HOST, NEW_API_KEY
    )

    new_allofpolicy = FirewallReplace(
        allofpolicy,
        allfirewallruleidnew1,
        allfirewallruleidnew2,
        firewallruleid,
        allfirewallruleidold,
        allfirewallcustomrule,
        t1statefulid,
        t2statefulid,
    )
    return new_allofpolicy
