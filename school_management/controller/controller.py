from odoo import http

class Controllers(http.Controller):

    @http.route('/applications', auth='public', website=True, type='http')
    def applications(self, **kw):
        if http.request.session.login:
            if kw:
                print(kw)
                data = {
                    'name': kw['name'],
                    'phone': kw['phone'],
                    'mail': kw['mail'],
                    'age': kw['age'],
                    'gender': kw['gender'],
                    'dateOfBirth': kw['dateOfBirth'],
                    'class_id': int(kw['class_id']),
                    'address': kw['address'],
                    'state': kw['state'],
                    'city': kw['city'],
                    'zip': kw['zip'],
                    'uid': http.request.session.uid,
                    'states': 'draft'
                }

                http.request.env['s.application'].create(data)

                return http.request.redirect('/')
            else:
                if http.request.env['s.application'].search([('uid', '=', int(http.request.session.uid))]) or http.request.env['school.management'].search([('uid', '=', int(http.request.session.uid))]):
                    print('You Are Already Applied')
                    return http.request.redirect('/status')
                else:
                    res_partner_id = http.request.env['res.users'].search([('id', '=', int(http.request.session.uid))]).read(['partner_id'])
                    # print(res_partner_id[0]['partner_id'][0])
                    # print(http.request.session.uid)
                    res_partner = http.request.env['res.partner'].search([('id', '=', res_partner_id[0]['partner_id'][0])])
                    class_id = http.request.env['s.class'].search([])
                    # print(res_partner)
                    return http.request.render('school_management.applications', {
                        'res_partner': res_partner,
                        'class_id': class_id,
                    })



            # print(http.request.session)
            # try:
            #     if kw:
            #         print(kw)
            #         print(http.request.session.uid)
            #         return http.request.redirect('/')
            #     else:
            #         application = http.request.env['s.application'].search([])
            #         return http.request.render('school_management.applications', {})
            # except:
            #     print('Application Error')
            #     return 0
        else:
            return http.request.redirect('/web/login')

    # @http.route('/signup', auth='public', website=True, type='http')
    # def signup(self, **kw):
    #     try:
    #         if kw:
    #             print(kw)
    #             print(http.request.params['name'])
    #             return http.request.redirect('/login')
    #         else:
    #             print('No kw, Load Sign Up page')
    #             return http.request.render('school_management.signup', {})
    #     except:
    #         print('/signup Terminated')
    #         return 0
    #
    # @http.route('/login', auth='public', website=True, type='http')
    # def login(self, **kw):
    #     return http.request.render('school_management.login', {})

    # @http.route('/signup/submit', auth='public', website=True, type='http')
    # def signupSubmit(self, **kw):
    #     print(kw)
    #     # return 0
    #     return http.request.redirect('/web/login')
    @http.route('/status', auth='public', website=True, type='http')
    def status(self, **kw):
        if http.request.session.login:
            if kw:
                print(kw)
                return http.request.redirect('/')
            else:
                if http.request.env['s.application'].search([('states', '=', 'admission'),('uid', '=', int(http.request.session.uid))]):
                    student_id = http.request.env['s.application'].search([('uid', '=', int(http.request.session.uid))])
                    return http.request.render('school_management.status_1', {
                        'student_id': student_id,
                    })
                elif http.request.env['school.management'].search([('uid', '=', int(http.request.session.uid))]):
                    if http.request.env['school.management'].search([('uid', '=', int(http.request.session.uid))]).read(['class_id'])[0]['class_id']:
                        class_id = http.request.env['school.management'].search([('uid', '=', int(http.request.session.uid))]).read(['class_id'])[0]['class_id'][1]
                    else:
                        class_id = "Not Assign"
                    print(class_id)
                    return http.request.render('school_management.status_2', {
                        'class_id': class_id
                    })
                elif http.request.env['s.application'].search([('states', '=', 'draft'),('uid', '=', int(http.request.session.uid))]):
                    return http.request.render('school_management.status_3', {})
                else:
                    return http.request.redirect('/')
        else:
            return http.request.redirect('/web/login')
