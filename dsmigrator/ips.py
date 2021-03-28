import json
import urllib3
import requests

cert = False


def ips_rules_transform(
    allofpolicy,
    t1portlistid,
    t2portlistid,
    OLD_HOST,
    OLD_API_KEY,
    NEW_HOST,
    NEW_API_KEY,
):
    og_ipsruleid = IPSGet(allofpolicy)
    og_ipsappid = IPSappGet(allofpolicy)

    allipsapp, allipsappidnew1, allipsappidold, allipscustomapp = IPSappDescribe(
        og_ipsappid,
        t1portlistid,
        t2portlistid,
        OLD_HOST,
        OLD_API_KEY,
        NEW_HOST,
        NEW_API_KEY,
    )

    allipsappidnew2 = IPSappCustom(allipsapp, allipscustomapp, NEW_HOST, NEW_API_KEY)

    allipsrule, allipsruleidnew1, allipsruleidold, allipscustomrule = IPSDescribe(
        og_ipsruleid,
        og_ipsappid,
        allipsappidnew1,
        allipsappidnew2,
        allipsappidold,
        allipscustomapp,
        OLD_HOST,
        OLD_API_KEY,
        NEW_HOST,
        NEW_API_KEY,
    )

    allipsruleidnew2 = IPSCustom(allipsrule, allipscustomrule, NEW_HOST, NEW_API_KEY)

    aop_replace_ips_rules = IPSReplace(
        allofpolicy,
        allipsruleidnew1,
        allipsruleidnew2,
        og_ipsruleid,
        allipsruleidold,
        allipscustomrule,
    )
    aop_replace_ips_apps = IPSappReplace(
        aop_replace_ips_rules,
        allipsappidnew1,
        allipsappidnew2,
        og_ipsappid,
        allipsappidold,
        allipscustomapp,
    )
    final = aop_replace_ips_apps
    return final


def IPSappGet(allofpolicy):
    ipsappid = []
    print("IPS application types in Tenant 1", flush=True)
    for describe in allofpolicy:
        namejson = json.loads(describe)
        if "applicationTypeIDs" in namejson["intrusionPrevention"]:
            for count, here2 in enumerate(
                namejson["intrusionPrevention"]["applicationTypeIDs"]
            ):
                ipsappid.append(str(here2))
    ipsappid = list(dict.fromkeys(ipsappid))
    print(ipsappid, flush=True)
    return ipsappid


def IPSappDescribe(
    ipsappid,
    t1portlistid,
    t2portlistid,
    url_link_final,
    tenant1key,
    url_link_final_2,
    tenant2key,
):
    allipsapp = []
    allipsappname = []
    allipsappidnew1 = []
    allipsappidold = []
    allipscustomapp = []
    print("Searching IPS application types in Tenant 1...", flush=True)
    if ipsappid:
        for count, dirlist in enumerate(ipsappid):
            payload = {}
            url = url_link_final + "api/applicationtypes/" + str(dirlist)
            headers = {
                "api-secret-key": tenant1key,
                "api-version": "v1",
                "Content-Type": "application/json",
            }
            response = requests.request(
                "GET", url, headers=headers, data=payload, verify=cert
            )
            describe = str(response.text)
            allipsapp.append(describe)
            ipsappjson = json.loads(describe)
            allipsappname.append(str(ipsappjson["name"]))
            print(
                "#"
                + str(count)
                + " IPS Application Type name: "
                + str(ipsappjson["name"]),
                flush=True,
            )
            index3 = describe.find("portListID")
            if index3 != -1:
                indexpart = describe[index3 + 10 :]
                startIndex = indexpart.find(":")
                if startIndex != -1:  # i.e. if the first quote was found
                    endIndex3 = indexpart.find(",", startIndex + 1)
                    if (
                        startIndex != -1 and endIndex3 != -1
                    ):  # i.e. both quotes were found
                        indexid1 = indexpart[startIndex + 1 : endIndex3]
                        indexid5 = describe[index3 : index3 + 10 + endIndex3]
                        indexnum = t1portlistid.index(indexid1)
                        listpart = indexid5.replace(indexid1, t2portlistid[indexnum])
                        allipsapp[count] = describe.replace(indexid5, listpart)
            print("#" + str(count) + " IPS Application Type ID: " + dirlist, flush=True)
    print("Done!", flush=True)
    print("Searching and Modifying IPS application types in Tenant 2...", flush=True)
    for count, dirlist in enumerate(allipsappname):
        payload = (
            '{"searchCriteria": [{"fieldName": "name","stringValue": "'
            + dirlist
            + '"}]}'
        )
        url = url_link_final_2 + "api/applicationtypes/search"
        headers = {
            "api-secret-key": tenant2key,
            "api-version": "v1",
            "Content-Type": "application/json",
        }
        response = requests.request(
            "POST", url, headers=headers, data=payload, verify=cert
        )
        describe = str(response.text)
        taskjson = json.loads(describe)
        if not "message" in taskjson:
            index = describe.find(dirlist)
            if index != -1:
                index = describe.find('"ID"')
                if index != -1:
                    indexpart = describe[index + 4 :]
                    startIndex = indexpart.find(":")
                    if startIndex != -1:  # i.e. if the first quote was found
                        endIndex = indexpart.find("}", startIndex + 1)
                        if (
                            startIndex != -1 and endIndex != -1
                        ):  # i.e. both quotes were found
                            indexid = indexpart[startIndex + 1 : endIndex]
                            allipsappidnew1.append(str(indexid))
                            allipsappidold.append(count)
                            payload = allipsapp[count]
                            url = (
                                url_link_final_2
                                + "api/applicationtypes/"
                                + str(indexid)
                            )
                            headers = {
                                "api-secret-key": tenant2key,
                                "api-version": "v1",
                                "Content-Type": "application/json",
                            }
                            response = requests.request(
                                "POST", url, headers=headers, data=payload, verify=cert
                            )
                            print(
                                "#"
                                + str(count)
                                + " IPS Application Type ID: "
                                + indexid,
                                flush=True,
                            )
                else:
                    print(describe, flush=True)
                    print(payload, flush=True)
            else:
                allipscustomapp.append(count)
        else:
            print(describe, flush=True)
            print(payload, flush=True)
    print("Done!", flush=True)
    return allipsapp, allipsappidnew1, allipsappidold, allipscustomapp


def IPSappCustom(allipsapp, allipscustomapp, url_link_final_2, tenant2key):
    allipsappidnew2 = []
    if allipscustomapp:
        print("Creating IPS application Type Custom Rule...", flush=True)
        for count, indexnum in enumerate(allipscustomapp):
            payload = allipsapp[indexnum]
            url = url_link_final_2 + "api/applicationtypes"
            headers = {
                "api-secret-key": tenant2key,
                "api-version": "v1",
                "Content-Type": "application/json",
            }
            response = requests.request(
                "POST", url, headers=headers, data=payload, verify=cert
            )
            describe = str(response.text)
            index = describe.find('"ID"')
            if index != -1:
                indexpart = describe[index + 4 :]
                startIndex = indexpart.find(":")
                if startIndex != -1:  # i.e. if the first quote was found
                    endIndex = indexpart.find("}", startIndex + 1)
                    if (
                        startIndex != -1 and endIndex != -1
                    ):  # i.e. both quotes were found
                        indexid = indexpart[startIndex + 1 : endIndex]
                        allipsappidnew2.append(str(indexid))
                        print(
                            "#"
                            + str(count)
                            + " IPS Application Type ID: "
                            + str(indexid),
                            flush=True,
                        )
            else:
                print(describe, flush=True)
                print(payload, flush=True)
        print("Done!", flush=True)
    return allipsappidnew2


def IPSappReplace(
    allofpolicy,
    allipsappidnew1,
    allipsappidnew2,
    ipsappid,
    allipsappidold,
    allipscustomapp,
):
    for count, describe in enumerate(allofpolicy):
        taskjson = json.loads(describe)
        if "applicationTypeIDs" in taskjson["intrusionPrevention"]:
            if allipsappidnew1 or allipsappidnew2:
                for count1, this in enumerate(
                    taskjson["intrusionPrevention"]["applicationTypeIDs"]
                ):
                    checkindex = ipsappid.index(str(this))
                    if checkindex in allipsappidold:
                        checkindex1 = allipsappidold.index(checkindex)
                        taskjson["intrusionPrevention"]["applicationTypeIDs"][
                            count1
                        ] = allipsappidnew1[checkindex1]
                    elif checkindex in allipscustomapp:
                        checkindex1 = allipscustomapp.index(checkindex)
                        taskjson["intrusionPrevention"]["applicationTypeIDs"][
                            count1
                        ] = allipsappidnew2[checkindex1]
        allofpolicy[count] = json.dumps(taskjson)
    return allofpolicy


def IPSGet(allofpolicy):
    ipsruleid = []
    print("IPS rules in Tenant 1", flush=True)
    for describe in allofpolicy:
        namejson = json.loads(describe)
        if "ruleIDs" in namejson["intrusionPrevention"]:
            for count, here2 in enumerate(namejson["intrusionPrevention"]["ruleIDs"]):
                ipsruleid.append(str(here2))
    ipsruleid = list(dict.fromkeys(ipsruleid))
    print(ipsruleid, flush=True)
    return ipsruleid


def IPSDescribe(
    ipsruleid,
    ipsappid,
    allipsappidnew1,
    allipsappidnew2,
    allipsappidold,
    allipscustomapp,
    url_link_final,
    tenant1key,
    url_link_final_2,
    tenant2key,
):
    allipsrule = []
    allipsrulename = []
    allipsruleidnew1 = []
    allipsruleidold = []
    allipscustomrule = []
    print("Searching IPS rules in Tenant 1...", flush=True)
    if ipsruleid:
        for count, dirlist in enumerate(ipsruleid):
            payload = {}
            url = url_link_final + "api/intrusionpreventionrules/" + str(dirlist)
            headers = {
                "api-secret-key": tenant1key,
                "api-version": "v1",
                "Content-Type": "application/json",
            }
            response = requests.request(
                "GET", url, headers=headers, data=payload, verify=cert
            )
            describe = str(response.text)
            allipsrule.append(describe)
            ipsjson = json.loads(describe)
            allipsrulename.append(str(ipsjson["name"]))
            print(
                "#" + str(count) + " IPS rule name: " + str(ipsjson["name"]), flush=True
            )
            index3 = describe.find("applicationTypeID")
            if index3 != -1:
                indexpart = describe[index3 + 17 :]
                startIndex = indexpart.find(":")
                if startIndex != -1:  # i.e. if the first quote was found
                    endIndex3 = indexpart.find(",", startIndex + 1)
                    if (
                        startIndex != -1 and endIndex3 != -1
                    ):  # i.e. both quotes were found
                        indexid1 = indexpart[startIndex + 1 : endIndex3]
                        checkindex = ipsappid.index(indexid1)
                        if checkindex in allipsappidold:
                            checkindex1 = allipsappidold.index(checkindex)
                            replaceid = allipsappidnew1[checkindex1]
                        elif checkindex in allipscustomapp:
                            checkindex1 = allipscustomapp.index(checkindex)
                            replaceid = allipsappidnew2[checkindex1]
                        indexid5 = describe[index3 : index3 + 17 + endIndex3]
                        listpart = indexid5.replace(indexid1, replaceid)
                        allipsrule[count] = describe.replace(indexid5, listpart)
            print("#" + str(count) + " IPS rule ID: " + dirlist, flush=True)
    print("Done!", flush=True)
    print("Searching and Modifying IPS rule in Tenant 2...", flush=True)
    for count, dirlist in enumerate(allipsrulename):
        payload = (
            '{"searchCriteria": [{"fieldName": "name","stringValue": "'
            + dirlist
            + '"}]}'
        )
        url = url_link_final_2 + "api/intrusionpreventionrules/search"
        headers = {
            "api-secret-key": tenant2key,
            "api-version": "v1",
            "Content-Type": "application/json",
        }
        response = requests.request(
            "POST", url, headers=headers, data=payload, verify=cert
        )
        describe = str(response.text)
        taskjson = json.loads(describe)
        if not "message" in taskjson:
            index = describe.find(dirlist)
            if index != -1:
                index = describe.find('"ID"')
                if index != -1:
                    indexpart = describe[index + 4 :]
                    startIndex = indexpart.find(":")
                    if startIndex != -1:  # i.e. if the first quote was found
                        endIndex = indexpart.find(",", startIndex + 1)
                        if (
                            startIndex != -1 and endIndex != -1
                        ):  # i.e. both quotes were found
                            indexid = indexpart[startIndex + 1 : endIndex]
                            allipsruleidnew1.append(str(indexid))
                            allipsruleidold.append(count)
                            print(
                                "#" + str(count) + " IPS rule ID: " + str(indexid),
                                flush=True,
                            )
                        else:
                            endIndex = indexpart.find("}", startIndex + 1)
                            if (
                                startIndex != -1 and endIndex != -1
                            ):  # i.e. both quotes were found
                                indexid = indexpart[startIndex + 1 : endIndex]
                                allipsruleidnew1.append(str(indexid))
                                allipsruleidold.append(count)
                                print(
                                    "#" + str(count) + " IPS rule ID: " + str(indexid),
                                    flush=True,
                                )
                else:
                    print(describe, flush=True)
                    print(payload, flush=True)
            else:
                allipscustomrule.append(count)
        else:
            print(describe, flush=True)
            print(payload, flush=True)
    print("Done!", flush=True)
    # print("Tenant 2 default IPS rules", flush=True)
    # print(allipsruleidnew1, flush=True)
    return allipsrule, allipsruleidnew1, allipsruleidold, allipscustomrule


def IPSCustom(allipsrule, allipscustomrule, url_link_final_2, tenant2key):
    allipsruleidnew2 = []
    if allipscustomrule:
        print("Creating new custom IPS rule in Tenant 2...", flush=True)
        for count, indexnum in enumerate(allipscustomrule):
            payload = allipsrule[indexnum]
            url = url_link_final_2 + "api/intrusionpreventionrules"
            headers = {
                "api-secret-key": tenant2key,
                "api-version": "v1",
                "Content-Type": "application/json",
            }
            response = requests.request(
                "POST", url, headers=headers, data=payload, verify=cert
            )
            describe = str(response.text)
            index = describe.find('"ID"')
            if index != -1:
                indexpart = describe[index + 4 :]
                startIndex = indexpart.find(":")
                if startIndex != -1:  # i.e. if the first quote was found
                    endIndex = indexpart.find(",", startIndex + 1)
                    if (
                        startIndex != -1 and endIndex != -1
                    ):  # i.e. both quotes were found
                        indexid = indexpart[startIndex + 1 : endIndex]
                        allipsruleidnew2.append(str(indexid))
                        print(
                            "#" + str(count) + " IPS rule ID: " + str(indexid),
                            flush=True,
                        )
                    else:
                        endIndex = indexpart.find("}", startIndex + 1)
                        if (
                            startIndex != -1 and endIndex != -1
                        ):  # i.e. both quotes were found
                            indexid = indexpart[startIndex + 1 : endIndex]
                            allipsruleidnew2.append(str(indexid))
                            print(
                                "#" + str(count) + " IPS rule ID: " + str(indexid),
                                flush=True,
                            )
            else:
                print(describe, flush=True)
                print(payload, flush=True)
        print("Done!", flush=True)
    # print("all new IPS rule custom rule", flush=True)
    # print(allipsruleidnew2, flush=True)
    return allipsruleidnew2


def IPSReplace(
    allofpolicy,
    allipsruleidnew1,
    allipsruleidnew2,
    ipsruleid,
    allipsruleidold,
    allipscustomrule,
):
    for count, describe in enumerate(allofpolicy):
        index = describe.find('"intrusionPrevention"')
        if index != -1:
            indexpart = describe[index + 20 :]
            startIndex = indexpart.find("}")
            if startIndex != -1:  # i.e. if the first quote was found
                endIndex = indexpart.find("}", startIndex + 1)
                if startIndex != -1 and endIndex != -1:  # i.e. both quotes were found
                    indexid = indexpart[startIndex + 1 : endIndex]
                    index2 = indexid.find("ruleIDs")
                    if index2 != -1:
                        indexpart2 = indexid[index2 + 9 :]
                        startIndex2 = indexpart2.find("[")
                        if startIndex2 != -1:  # i.e. if the first quote was found
                            endIndex2 = indexpart2.find("]", startIndex2 + 1)
                            if (
                                startIndex2 != -1 and endIndex2 != -1
                            ):  # i.e. both quotes were found
                                indexid2 = indexpart2[startIndex2 + 1 : endIndex2]
                                indexid3 = indexpart2[startIndex2 + 1 : endIndex2]
                                indexid2.replace(", ", ",")
                                indexid4 = indexid2.split(",")
                                if allipsruleidnew1 or allipsruleidnew2:
                                    for count1, this in enumerate(indexid4):
                                        checkindex = ipsruleid.index(this)
                                        if checkindex in allipsruleidold:
                                            checkindex1 = allipsruleidold.index(
                                                checkindex
                                            )
                                            indexid4[count1] = allipsruleidnew1[
                                                checkindex1
                                            ]
                                        elif checkindex in allipscustomrule:
                                            checkindex1 = allipscustomrule.index(
                                                checkindex
                                            )
                                            indexid4[count1] = allipsruleidnew2[
                                                checkindex1
                                            ]
                                    indexid2 = ",".join(indexid4)
                                modulepart = describe[index : index + 20 + endIndex]
                                modulepart2 = modulepart.replace(indexid3, indexid2)
                                allofpolicy[count] = describe.replace(
                                    modulepart, modulepart2
                                )
    return allofpolicy
