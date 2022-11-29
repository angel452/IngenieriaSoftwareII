select * from my_library_mybuyedproducts;


delete from my_library_mybuyedproducts where usuario_comprador_id =1;

select * from account_wallet;

select * from orders_order;

select * from orders_orderitem;

select * from pixelsaurapp_product;

delete from pixelsaurapp_product where available = true;

select * from coupons_coupon;
delete from coupons_coupon where id = 7;
select * from account_wallet;
delete from pixelsaurapp_calificacion where created_by_id= 1;
select * from pixelsaurapp_calificacion;
select * from pixelsaurapp_regalo;
delete from pixelsaurapp_regalo where id = 24;
SELECT * from my_library_mybuyedproducts;
delete from my_library_mybuyedproducts where id = 7;
alter table pixelsaurapp_calificacion rename created_by to created_by_id;
