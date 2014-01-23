from redmine.api import Api


class Ticket:

    @staticmethod
    def getTickets(ticketsIdsList, headers=None):
        if len(ticketsIdsList) == 0:
            return {'header': [], 'data': []}
        if not headers:
            headers = ['id', 'project_name', 'subject', 'priority_name', 'status_name', 'assigned_to_name']

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
                    if type(parameter[1]) is dict and 'name' in parameter[1]:
                        formated_issue[parameter[0] + '_name'] = parameter[1]['name']
                # remove some key
                keys_to_remove = list()
                for key in formated_issue:
                    if key not in headers:
                        keys_to_remove.append(key)
                for key in keys_to_remove:
                    formated_issue.pop(key, None)
                if 'assigned_to_name' not in formated_issue:
                    formated_issue['assigned_to_name'] = ''
                results.append(formated_issue)

        return {'header': headers, 'data': results}
