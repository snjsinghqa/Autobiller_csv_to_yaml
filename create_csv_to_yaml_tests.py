import yaml
import datetime
import csv
#  user only need to pass Billweb file name


class CreateTestsYaml():
    billweb_users_file = 'autobiller_renewal_referral_10_11_2018.csv'
    billweb_users_file_path = 'input_csv/'+billweb_users_file
    renew_template = 'templates/renew_template.yaml'
    retry_template = 'templates/retry_template.yaml'

    def __init_(self):
        pass

    def create_yaml(self):
        '''
        Create autobiller tests yaml
        Read Billweb CSV and dump yaml data generated using renewal and retry templates
        into autobiller tests using renewal

        :return:
        '''
        import time
        timestr = time.strftime("%Y%m%d-%H%M%S")
        billweb_users_file = self.billweb_users_file.split('.')[0]
        tests_yaml_name_renewal = 'output_yaml/' + billweb_users_file + '_tests_renewal' + '.yaml'
        tests_yaml_name_retry = 'output_yaml/' + billweb_users_file + '_tests_retry' + '.yaml'
        with open(self.billweb_users_file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    keys = row
                else:
                    test_data = dict(zip(keys, row))
                    renewal_data = self.renewal_test_data(test_data)

                    with open(tests_yaml_name_renewal, 'a') as outfile:
                        yaml.dump(renewal_data, outfile, default_flow_style=False)

                    retry_data = self.retry_test_data(test_data)
                    with open(tests_yaml_name_retry, 'a') as outfile:
                        yaml.dump(retry_data, outfile, default_flow_style=False)
                line_count += 1

    def renewal_test_data(self, test_data):
        yaml_template_data = yaml.load(open(self.renew_template))
        yaml_template_data[0]['update']['user_id'][int(test_data['user_id'])] = \
            yaml_template_data[0]['update']['user_id'].pop('$user_id')
        yaml_template_data[0]['validate']['user_id'][int(test_data['user_id'])] = \
            yaml_template_data[0]['validate']['user_id'].pop('$user_id')
        yaml_template_data[0]['finalize']['user_id'][int(test_data['user_id'])] = \
            yaml_template_data[0]['finalize']['user_id'].pop('$user_id')
        yaml_template_data[0]['update']['user_id'][int(test_data['user_id'])]['user.is_paid'] = True
        yaml_template_data[0]['validate']['user_id'][int(test_data['user_id'])]['user.is_paid'] = True
        yaml_template_data[0]['validate']['user_id'][int(test_data['user_id'])]['user.is_paid'] = True
        yaml_template_data[0]['validate']['user_id'][int(test_data['user_id'])]['user.package_id'] = \
            int(test_data['ending_package'])
        yaml_template_data[0]['validate']['user_id'][int(test_data['user_id'])]['user.payment_processor_id'] = \
            int(test_data['payment_processor_id'])
        yaml_template_data[0]['validate']['tran_id']['latest']['tran.payment_method_id'] = \
            int(test_data['payment_method_id'])
        yaml_template_data[0]['validate']['tran_id']['latest']['tran.tranx_status_id'] = \
            int(test_data['tranxStatus_id'])
        yaml_template_data[0]['validate']['tran_id']['latest']['tran.total'] = \
            int(int(test_data['trans_total'])*100)
        trans_total_after_discount = (test_data.get('trans_total_after_discount'))
        if trans_total_after_discount is not None:
            trans_total_after_discount = float(trans_total_after_discount)
            trans_total_after_discount = int(self.round_number(trans_total_after_discount))
            yaml_template_data[0]['validate']['tran_id']['latest']['tran.total'] = trans_total_after_discount
        else:
            trans_total = int(test_data['trans_total'])
            trans_total = int(self.round_number(trans_total))
            yaml_template_data[0]['validate']['tran_id']['latest']['tran.total'] = trans_total
        yaml_template_data[0]['tc_name'] = test_data['username']

        return yaml_template_data

    def retry_test_data(self, test_data):
        yaml_template_data = yaml.load(open(self.retry_template))
        yaml_template_data[0]['update']['user_id'][int(test_data['user_id'])] = \
            yaml_template_data[0]['update']['user_id'].pop('$user_id')
        yaml_template_data[0]['validate']['user_id'][int(test_data['user_id'])] = \
            yaml_template_data[0]['validate']['user_id'].pop('$user_id')
        yaml_template_data[0]['update']['user_id'][int(test_data['user_id'])]['user.is_paid'] = False
        yaml_template_data[0]['validate']['user_id'][int(test_data['user_id'])]['user.is_paid'] = True
        yaml_template_data[0]['validate']['user_id'][int(test_data['user_id'])]['user.is_paid'] = True
        yaml_template_data[0]['validate']['user_id'][int(test_data['user_id'])]['user.package_id'] = \
            int(test_data['ending_package'])
        yaml_template_data[0]['validate']['user_id'][int(test_data['user_id'])]['user.payment_processor_id'] = \
            int(test_data['payment_processor_id'])
        yaml_template_data[0]['validate']['tran_id']['latest']['tran.payment_method_id'] = \
            int(test_data['payment_method_id'])
        yaml_template_data[0]['validate']['tran_id']['latest']['tran.tranx_status_id'] = \
            int(test_data['tranxStatus_id'])
        yaml_template_data[0]['validate']['tran_id']['latest']['tran.total'] = int(int(test_data['trans_total']) * 100)
        trans_total_after_discount = (test_data.get('trans_total_after_discount'))
        if trans_total_after_discount is not None:
            trans_total_after_discount = float(trans_total_after_discount)
            trans_total_after_discount = int(self.round_number(trans_total_after_discount))
            yaml_template_data[0]['validate']['tran_id']['latest']['tran.total'] = trans_total_after_discount
        else:
            trans_total = int(test_data['trans_total'])
            trans_total = int(self.round_number(trans_total))
            yaml_template_data[0]['validate']['tran_id']['latest']['tran.total'] = trans_total
        yaml_template_data[0]['tc_name'] = test_data['username']

        return yaml_template_data

    def round_number(self, num):
        if type(num) == int:
            num = str(num)
            if len(num) <= 5:
                num_diff = int(5 - len(num))
                for c in range(num_diff):
                    num = int(num) * 10
        elif type(num) == float:
            num = str(num)
            num = num.replace('.', '')
            if len(num) <= 5:
                num_diff = int(5 - len(num))
                for c in range(num_diff):
                    num = int(num) * 10
        return num


new_tests = CreateTestsYaml()
new_tests.create_yaml()
