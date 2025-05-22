from admin_tools.menu import items, Menu

class CustomMenu(Menu):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.children += [
            items.MenuItem('Dashboard', '/admin/'),
            items.AppList('Applications', exclude=('django.contrib.*',)),
            items.AppList('Administration', models=('django.contrib.*',)),
        ]
