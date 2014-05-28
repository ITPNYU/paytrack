from paytrack import *
Base.metadata.create_all(engine)

u_m = User(netid='mly2')
db_session.add(u_m)
u_k = User(netid='kw1213')
db_session.add(u_k)

account_camp = Account(name='ITP Camp', paygate_form='1589')
db_session.add(account_camp)
db_session.commit()

payer_a = Payer(fname='A', lname='B', email='a.b@example.com')
db_session.add(payer_a)
payer_c = Payer(fname='C', lname='D', email='c.d@example.com')
db_session.add(payer_c)
payer_e = Payer(fname='E', lname='F', email='e.f@example.com')
db_session.add(payer_e)
payer_g = Payer(fname='G', lname='H', email='g.h@example.com')
db_session.add(payer_g)
payer_i = Payer(fname='I', lname='J', email='i.j@example.com')
db_session.add(payer_i)
payer_k = Payer(fname='K', lname='L', email='k.l@example.com')
db_session.add(payer_k)
db_session.commit()

invoice_a = Invoice(status='sent', amount=900, payer=payer_a, account=account_camp)
db_session.add(invoice_a)
invoice_c = Invoice(status='sent', amount=600, payer=payer_c, paid=True, account=account_camp)
db_session.add(invoice_c)
invoice_e = Invoice(status='sent', amount=600, payer=payer_e, account=account_camp)
db_session.add(invoice_e)
invoice_g = Invoice(status='sent', amount=1200, payer=payer_g, account=account_camp)
db_session.add(invoice_g)
invoice_i = Invoice(status='sent', amount=1200, payer=payer_i, account=account_camp)
db_session.add(invoice_i)
invoice_k = Invoice(status='draft', amount=1200, payer=payer_k, account=account_camp)
db_session.add(invoice_i)
db_session.commit()

payment_a = Payment(status='paid', amount=900, payment_type='creditcard', account=account_camp,
                    trans_decision='ACCEPT', trans_reference='1396383715201', trans_id='228132',
                    trans_time='2014-04-01T202155Z', trans_sig='t4wa1YimEbc347bWyWFyxCUO/8w=',
                    payer=payer_a, invoice=invoice_a)
db_session.add(payment_a)
payment_c = Payment(status='paid', amount=600, payment_type='creditcard', account=account_camp,
                    trans_decision='ACCEPT', trans_reference='1396451085531', trans_id='228315',
                    trans_time='2014-04-02T150451Z', trans_sig='W8WBoeHi1pGPDwVeeGqjC4az6Cg=',
                    payer=payer_c, invoice=invoice_c)
db_session.add(payment_c)
payment_e = Payment(status='paid', amount=600, payment_type='creditcard', account=account_camp,
                    trans_decision='ACCEPT', trans_reference='1396458088715', trans_id='228340',
                    trans_time='2014-04-02T170129Z', trans_sig='3SyZW291IdS1+TOo7BvingU0GoA=',
                    payer=payer_e, invoice=invoice_e)
db_session.add(payment_e)
payment_g = Payment(status='paid', amount=1200, payment_type='creditcard', account=account_camp,
                    trans_decision='ACCEPT', trans_reference='1400620714007', trans_id='237540',
                    trans_time='2014-05-20T211834Z', trans_sig='r8oW7p2ht5jDS9YTgwgy8aamip8=',
                    payer=payer_g, invoice=invoice_g)
db_session.add(payment_g)
payment_i = Payment(status='error', payment_type='creditcard', account=account_camp,
                    trans_decision='ERROR', trans_time='2014-05-21T191834Z',
                    payer_id=payer_i.id, invoice=invoice_i)
db_session.add(payment_i)
db_session.commit()

refund_a = Refund(status='approved', amount=900, payer=payer_a, payment=payment_a, reviewer=u_m,
                  note='not coming')
db_session.add(refund_a)
refund_g = Refund(status='approved', amount=300, payer=payer_g, payment=payment_g, reviewer=u_m,
                  note='early bird discount')
db_session.add(refund_g)
credit_c = Credit(status='approved', amount=600, credit_type='discount', payer=payer_c,
                  reviewer=u_m, note='instigator', account=account_camp)
db_session.add(credit_c)

db_session.commit()

