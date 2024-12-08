from django.shortcuts import render, redirect
import psycopg2
from .forms import RetailForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Customer, Wholesale
from retail_wholesale.func import (
    dbconnector,
    take_id_from_customer,
    take_id_from_product
)


@login_required
def retail_list(request):
    template = 'retail/retail_list.html'
    con = dbconnector()
    cur = con.cursor()
    if request.user.is_staff:
        cur.execute(
            ''' select * from retail_admin'''
        )
    else:
        cur.execute(
            ''' select * from retail_user'''
        )
    order_list = cur.fetchall()

    page = request.GET.get('page', 1)
    page = int(page)
    items_per_page = 10
    total_items = len(order_list)
    total_pages = (total_items + items_per_page - 1) // items_per_page

    if page < 1:
        page = 1
    elif page > total_pages:
        page = total_pages

    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    current_page_data = order_list[start_index:end_index]

    left = page - 2 if page - 2 > 0 else 1
    right = page + 2 if total_pages - page > 2 else total_pages

    context = {
        'page_obj': current_page_data,
        'current_page': page,
        'total_pages': total_pages,
        'pages': range(left, right + 1)
    }

    con.close()
    return render(request, template, context)


@login_required
def retail_detail(request, pk=None):
    template = 'retail/retail_detail.html'
    con = dbconnector()
    cur = con.cursor()
    cur.execute(
        f''' select 
	            w.id, w.sales,
	            p.category, p.sub_category, p.title, p.text
            from retail_wholesale w
	        join retail_product p
	            on w.product_id = p.id
            where w.id = {pk}'''
    )
    order = cur.fetchone()
    context = {'order': order}
    con.close()
    return render(request, template, context)


@login_required
def retail_add(request, pk=None):
    if not request.user.is_staff:
        raise PermissionDenied("У вас нет прав для доступа к этой странице.")
    else:
        if request.method == 'POST':
            form = RetailForm(request.POST)
            if form.is_valid():
                order_date = form.cleaned_data['order_date']
                region = form.cleaned_data['region']
                sales = form.cleaned_data['sales']
                customer = form.cleaned_data['customer']
                product = form.cleaned_data['product']

                customer_id = take_id_from_customer(
                    customer.first_name,
                    customer.second_name,
                    customer.phone_number
                )

                product_id = take_id_from_product(
                    product.category,
                    product.sub_category, 
                    product.title
                )
                print(order_date.strftime("%Y-%m-%d %H:%M:%S"))
                con = dbconnector()
                cur = con.cursor()
                if pk is not None:
                    cur.execute(f'''
                        call update_retail_wholesale(
                            {pk},
                            \'{order_date}\',
                            \'{region}\',
                            {sales},
                            {customer_id},
                            {product_id}
                        )
                    ''')
                else:
                    cur.execute(f'''
                        call insert_retail_wholesale(
                            \'{order_date}\',
                            \'{region}\',
                            {sales},
                            {customer_id},
                            {product_id}
                        )
                    ''')
                con.commit()
                con.close()

                return redirect('retail:retail_list')
        else:
            if pk is not None:
                con = dbconnector()
                cur = con.cursor()
                cur.execute(f'''
                    select * 
                    from retail_wholesale
                    where id = {pk};
                ''')
                data = cur.fetchone()
                con.close()
        
                form = RetailForm(initial={
                    'order_date': data[1].strftime("%Y-%m-%d"),
                    'region': data[2],
                    'sales': data[3],
                    'customer': data[4],
                    'product': data[5],
                })
            else:
                form = RetailForm()

        template = 'retail/retail_add.html'
        context = {'form': form}
        return render(request, template, context)
    

@login_required
def retail_delete(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied("У вас нет прав для доступа к этой странице.")
    else:
        con = dbconnector()
        cur = con.cursor()
        cur.execute(
            f''' select * from retail_wholesale w
            join retail_customer c on c.id = w.customer_id
            join retail_product p on p.id = w.product_id
                where w.id = {pk}'''
        )
        data = cur.fetchone()
        con.close()

        context = {'order': data}
        # Если был получен POST-запрос...
        if request.method == 'POST':
            con = dbconnector()
            cur = con.cursor()
            cur.execute(
                f''' delete from retail_wholesale
                where id = {pk}'''
            )
            con.commit()
            con.close()
            # ...и переадресовываем пользователя на страницу со списком записей.
            return redirect('retail:retail_list')
        # Если был получен GET-запрос — отображаем форму.
        return render(request, 'retail/retail_confirm_delete.html', context)


@login_required
def product_list(request):
    template = 'retail/retail_product_list.html'
    con = dbconnector()
    cur = con.cursor()
    if request.user.is_staff:
        cur.execute(
                ''' select distinct
                a.category,
                a.sub_category,
                a.title,
                d.sale_group
                from retail_admin a
                join do_task('retail_admin') d
                    on a.title = d.title
                order by a.title'''
        )
    else:
        cur.execute(
            ''' select distinct
                a.category,
                a.sub_category,
                a.title,
                d.sale_group
                from retail_user a
                join do_task('retail_user') d
                    on a.title = d.title
                order by a.title'''
        )
    
    products = cur.fetchall()
    con.close()

    context = {
        'products': products,
    }
    return render(request, template, context)
