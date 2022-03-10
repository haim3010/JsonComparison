import json


def compare_object_identical(infra_object, cloud_object):
    result = dict()
    result['CloudResourceItem'] = cloud_object
    result['IacResourceItem'] = infra_object
    result['state'] = 'Match' # default state
    result['ChangeLog'] = []

    if cloud_object['id'] == infra_object['id']:

        # matching ids
        for key in cloud_object.keys():
            if key in infra_object.keys() and cloud_object[key] != infra_object[key]:
                result['state'] = 'modified'
                result['ChangeLog'].append({'id': infra_object['id'],
                                            'KeyName': key,
                                            'CloudValue': cloud_object[key],
                                            'IacValue': infra_object[key]
                                            })
        if result['state'] == 'Match':
            result['ChangeLog'].append({'id': infra_object['id']})

    else:
        return -1 # Missing object

    return result


if __name__ == '__main__':
    with open('data/iac_resources.json') as fd:
        iac_data = json.load(fd)
    with open('data/cloud_resources.json') as fd:
        cloud_data = json.load(fd)

    matches_list = []
    missing_list = []
    modified_list = []

    Matches = 0
    Modifies = 0
    Misses = 0


    missing_object = dict()
    missing_object['CloudResourceItem'] = {}
    missing_object['IacResourceItem'] = {}
    missing_object['state'] = 'Missing'
    missing_object['ChangeLog'] = []

    for cloud_item in cloud_data:
        not_match_or_modified = True
        for iac_item in iac_data:
            res = compare_object_identical(iac_item, cloud_item)
            if isinstance(res, dict) and res['state'] == 'Match': # checking if res return dict
                matches_list.append(res)
                not_match_or_modified = False
                Matches +=1
                print("Match was found")
                break  # exiting inner loop
            elif isinstance(res, dict) and res['state'] == 'modified': # checking if res return dict
                modified_list.append(res)
                not_match_or_modified = False
                Modifies +=1
                print("modified was found")
                break  # exiting inner loop
        # Missing:
        if not_match_or_modified:
            item = {'id': cloud_item['id'],
                    'KeyName': cloud_item['name']}

            missing_object['ChangeLog'].append(item)
            missing_list.append(missing_object)
            print("mismatch was found")
            Misses +=1

    data = { 'Counter':{
                'Matches': Matches,
                'Modifies':Modifies,
                'Misses':Misses
    },
            'Match': matches_list,
            'Modified': modified_list,
            'Missing': missing_list}

    with open('analyzer.json', 'w') as fd:
        json.dump(data, fd, indent=2)
