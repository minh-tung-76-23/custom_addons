from odoo import http
from odoo.http import request

class InternOrderController(http.Controller):

    @http.route('/intern/order/approve/<int:order_id>', type='http', auth="public", website=True)
    def show_appointment_form(self, order_id, **kwargs):
        intern_order = request.env['intern.order'].sudo().browse(order_id)
        if not intern_order.exists():
            return request.not_found()
        return request.render('intern_pos_management.appointment_form_template', {
            'order': intern_order,
        })

    @http.route('/intern/order/approve/submit', type='http', auth="public", website=True, csrf=False)
    def submit_appointment_form(self, **post):
        order_id = int(post.get('order_id'))
        appointment_schedule = post.get('appointment_schedule')
        intern_order = request.env['intern.order'].sudo().browse(order_id)
        if intern_order.exists():
            intern_order.write({
                'appointment_schedule': appointment_schedule,
                'status': 'approved',
            })
            return request.render('intern_pos_management.appointment_success_template', {
                'order': intern_order,
            })
        return request.not_found()
    
    @http.route('/intern/order/reject/<int:order_id>', type='http', auth="public", website=True)
    def reject_order_res(self, order_id):
        """Xử lý yêu cầu từ đường link và cập nhật trạng thái"""
        order = request.env['intern.order'].sudo().browse(order_id)
        if order.exists():
            order.reject_order_convert()  # Gọi phương thức từ đối tượng order
            # Hiển thị thông báo trên một trang web
            return request.render('intern_pos_management.reject_order_template', {
                'message': "Cảm ơn bạn đã phản hồi. Chúng tôi sẽ tìm kiếm ứng viên khác phù hợp!",
            })
        else:
            return request.not_found("Không tìm thấy đơn thực tập.")