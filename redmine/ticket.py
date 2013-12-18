import core.consts as consts
import json
from api import Api


class Ticket:

    @staticmethod
    def getTickets(ticketsIdsList):

        if len(ticketsIdsList) == 0:
            return {'header': [], 'data': []}

        url = consts.serverUrls['ticketsList'] % {'tickets': ','.join(map(str, ticketsIdsList))}

        api = Api()
        results = list()

        for ticketId in ticketsIdsList:
            # XXX handle a full redmine response
            # then use configuration file to select what field to display (custom fields and all)
            # and order them
            issue = api.issue(ticketId)
            if 'issue' in issue:
                formated_issue = issue['issue']
                for parameter in formated_issue.items():
                    if type(parameter[1]) is dict and parameter[1].has_key('name'):
                        formated_issue[parameter[0] + '_name'] = parameter[1]['name']
                # remove some key
                keys_to_remove = (
                    'status',
                    'priority',
                    'custom_fields',
                    'parent',
                    'category',
                    'project',
                    'assigned_to',
                    'tracker',
                    'author',
                    'description',
                    'updated_on',
                    'done_ratio',

                    'tracker_name',
                    'category_name',
                    'author_name',
                    'created_on',
                    'start_date'
                )
                for key in keys_to_remove:
                    formated_issue.pop(key, None)
                if not formated_issue.has_key('assigned_to_name'):
                    formated_issue['assigned_to_name'] = ''
                results.append(formated_issue)

        #header = results[0].keys()
        # XXX forced headers
        header = ['id', 'project_name', 'subject', 'priority_name', 'status_name', 'assigned_to_name']

        return {'header': header, 'data': results}
