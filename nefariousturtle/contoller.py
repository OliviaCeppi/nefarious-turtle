from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Task,
    Subject,
    )


@view_config(route_name='home', renderer='view/mytemplate.pt')
def my_view(request):
    try:
        one = DBSession.query(Task).filter(Task.title == 'one').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'nefarious-turtle'}


@view_config(route_name='new_task', renderer='view/task_add.pt')
def new_task(request):
    if 'form.submitted' in request.params:
        title = request.params['title']
        task = Task(title=title)
        DBSession.add(task)

    return {}


@view_config(route_name='task_list', renderer='view/task_list.pt')
def all_task(request):
    tasks = DBSession.query(Task).all()
    return {'tasks': tasks}
#tel = {'jack': 4098, 'sape': 4139}


conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_nefarious-turtle_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

