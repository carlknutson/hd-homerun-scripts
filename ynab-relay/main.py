import os
import requests
import sys

ynab_api_url = 'https://api.ynab.com/v1'
ynab_token = os.environ['ynab_token']
ynab_budget_name = os.environ['ynab_budget_name']

def add_transaction(account, payee, amount):
    payee = 'Walmart' # 
    amount = 930
    transaction_account = 'Credit - Discover - 2nd'

    budgets = requests.get(url=f'{ynab_api_url}/budgets', params={'include_accounts': 'true'}, headers={'Authorization': f'Bearer {ynab_token}'}).json()['data']['budgets']
    budget_id = None
    account_id = None
    for budget in budgets:
        if budget['name'] == ynab_budget_name:
            budget_id = budget['id']
            for account in budget['accounts']:
                if account['name'] == transaction_account:
                    account_id = account['id']
    
    if not account_id:
        print(f'No account found with name {transaction_account}.')
        return

    transaction = {
        'transaction': {
            'account_id': account_id,
            'date': '2024-05-19',
            'amount': 12330,
            'payee_name': payee,
            'cleared': 'uncleared',
            'approved': False,
        }
    }

    transaction = requests.post(url=f'{ynab_api_url}/budgets/{budget_id}/transactions', json=transaction, headers={'Authorization': f'Bearer {ynab_token}'})
    transaction.raise_for_status

def get_accounts():
    accounts = []

    budgets = requests.get(url=f'{ynab_api_url}/budgets', params={'include_accounts': 'true'}, headers={'Authorization': f'Bearer {ynab_token}'}).json()['data']['budgets']
    for budget in budgets:
        if budget['name'] == ynab_budget_name:
            for account in budget['accounts']:
                if not (account['closed'] or account['deleted']):
                    accounts.append(account['name'])
    print(accounts)

def get_payees():
    payees = []

    budgets = requests.get(url=f'{ynab_api_url}/budgets', headers={'Authorization': f'Bearer {ynab_token}'}).json()['data']['budgets']
    for budget in budgets:
        if budget['name'] == ynab_budget_name:
            response = requests.get(url=f'{ynab_api_url}/budgets/{budget["id"]}/payees', headers={'Authorization': f'Bearer {ynab_token}'}).json()['data']['payees']
    
            for payee in response:
                print(payee)
                if not (payee['deleted'] or payee['transfer_account_id']):
                    payees.append(payee['name'])
            print(payees)
            return
    print(payees)

def main():
    try:
        action = sys.argv[1]
    except IndexError:
        print('An action parameter, must be provided.')
        return

    if action == 'add_transaction':
        add_transaction()
    elif action == 'get_payees':
        get_payees()
    elif action == 'get_accounts':
        get_accounts()
    else:
        print(f'Action: {action}, is not implemented.')

if __name__ == "__main__":
    main()
