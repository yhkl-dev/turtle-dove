from rest_framework.routers import DefaultRouter
from .views import GroupsViewset, UserGroupsViewset, GroupMembersViewset


group_router = DefaultRouter()
group_router.register(r'groups', GroupsViewset, basename="groups")
group_router.register(r'usergroups', UserGroupsViewset, basename="usergroups")
group_router.register(r'groupmembers', GroupMembersViewset, basename="groupmembers")
