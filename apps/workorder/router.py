from rest_framework.routers import DefaultRouter
from .views import (WorkOrderTaskViewset,
                    WorkOrderOperationViewset,
                    TemplateWorkOrderTaskFlowItemViewset,
                    TemplateWorkOrderTaskFlowViewset,
                    TemplateWorkOrderTypeViewset,
                    TemplateWorkOrderFlowTypeViewset,
                    TemplateWorkOrderProjectViewset,
                    TemplateWorkOrderModelViewset,
                    AuditWorkOrderTaskListViewset,
                    ExecWorkOrderTaskListViewset,
                    WorkOrderTaskStatusCodeViewset,
                    WorkOrderTaskOperationStatusCodeViewset,
                    WorkOrderTaskHistoryViewset,
                    WorkOrderHistoryCountViewSet,
                    WorkOrderTaskExecHistoryViewSet,
                    WorkOrderTaskAuditHistoryViewSet)


work_order_router = DefaultRouter()
work_order_router.register(r'workOrderTask', WorkOrderTaskViewset, base_name="workOrderTask")
work_order_router.register(r'workOrderOperation', WorkOrderOperationViewset, base_name="workOrderOperation")
work_order_router.register(r'templateWorkOrderTaskFlowItem', TemplateWorkOrderTaskFlowItemViewset, base_name="templateWorkOrderTaskFlowItem")
work_order_router.register(r'templateWorkOrderTaskFlow', TemplateWorkOrderTaskFlowViewset, base_name="templateWorkOrderTaskFlow")
work_order_router.register(r'templateWorkOrderType', TemplateWorkOrderTypeViewset, base_name="templateWorkOrderType")
work_order_router.register(r'templateWorkOrderFlowType', TemplateWorkOrderFlowTypeViewset, base_name="templateWorkOrderFlowType")
work_order_router.register(r'templateWorkOrderProject', TemplateWorkOrderProjectViewset, base_name="templateWorkOrderProject")
work_order_router.register(r'templateWorkOrderModel', TemplateWorkOrderModelViewset, base_name="templateWorkOrderModel")
work_order_router.register(r'auditWorkOrderTaskList', AuditWorkOrderTaskListViewset, base_name="auditWorkOrderTaskList")
work_order_router.register(r'execWorkOrderTaskList', ExecWorkOrderTaskListViewset, base_name="execWorkOrderTaskList")
work_order_router.register(r'workOrderTaskOperationStatusCode', WorkOrderTaskOperationStatusCodeViewset, base_name="workOrderTaskOperationStatusCode")
work_order_router.register(r'workOrderTaskStatusCode', WorkOrderTaskStatusCodeViewset, base_name="workOrderTaskStatusCode")
work_order_router.register(r'workOrderTaskHistory', WorkOrderTaskHistoryViewset, base_name="workOrderTaskHistory")
work_order_router.register(r'workOrderHistoryCount', WorkOrderHistoryCountViewSet, base_name="WorkOrderHistoryCountViewSet")
work_order_router.register(r'workOrderTaskExecHistory', WorkOrderTaskExecHistoryViewSet, base_name="workOrderTaskExecHistory")
work_order_router.register(r'workOrderTaskAuditHistory', WorkOrderTaskAuditHistoryViewSet, base_name="workOrderTaskAuditHistory")