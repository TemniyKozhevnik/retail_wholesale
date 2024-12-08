from django.shortcuts import render
from retail_wholesale.func import dbconnector
from django.contrib.auth.decorators import login_required


@login_required
def retail_analysis(request):
    template = 'analysis/analysis.html'
    action = request.GET.get('action')
    orders = ()
    if action == 'region':
        con = dbconnector()
        cur = con.cursor()
        if request.user.is_staff:
            cur.execute(
                    ''' select
                    region,
                    count(*),
                    sale_group
                    from do_task('retail_admin')
                    group by region, sale_group
                    order by sale_group asc, count desc'''
            )
        else:
            cur.execute(
                ''' select
                    region,
                    count(*),
                    sale_group
                    from do_task('retail_user')
                    group by region, sale_group
                    order by sale_group asc, count desc'''
            )
        orders = cur.fetchall()
        con.close()
    elif action == 'profit':
        con = dbconnector()
        cur = con.cursor()
        if request.user.is_staff:
            cur.execute(
                    ''' select
                    region,
                    sum(sales)
                    from do_task('retail_admin')
                    group by region
                    order by sum(sales) desc'''
            )
        else:
            cur.execute(
                ''' select
                    region,
                    sum(sales)
                    from do_task('retail_user')
                    group by region
                    order by sum(sales) desc'''
            )
        orders = cur.fetchall()
        con.close()
    elif action == 'product':
        con = dbconnector()
        cur = con.cursor()
        if request.user.is_staff:
            cur.execute(
                    ''' select distinct
                category,
                sub_category,
                title,
                sale_group,
				sum(sales)
                from do_task('retail_admin')
				group by title, category, sub_category, sale_group
                order by sum desc'''
            )
        else:
            cur.execute(
                ''' select distinct
                category,
                sub_category,
                title,
                sale_group,
				sum(sales)
                from do_task('retail_user')
				group by title, category, sub_category, sale_group
                order by sum desc'''
            )
        orders = cur.fetchall()
        con.close()
    context = {
        'orders': orders,
        'action': action
    }
    return render(request, template, context)