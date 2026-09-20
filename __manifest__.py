# -*- coding: utf-8 -*-
{
    'name': 'Jinasena : MasterData : Common',
    'version': '17.0.0.0.2',
    'summary': 'Master-data extracted from CDB for Common domain.',
    'description': 'Extracted from Clear-DB. Test-env master data. Edit the CSVs in data/ to add/remove rows before install.',
    'author': 'Jinasena Agricultural Machinery (Pvt) Ltd.',
    'category': 'Extra Tools',
    'license': 'LGPL-3',
    'depends': [
        'seed_master_data_and_settings',
        'BugFix-Studio-Misc',
        'bank-data',
        'studio_usermodel_migration',
    ],
    'data': [
        'data/res.currency.rate.csv',
        'data/res.company.csv',
        'data/res.bank.csv',
        'data/res.partner.bank.csv',
        'data/ir.sequence.csv',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
