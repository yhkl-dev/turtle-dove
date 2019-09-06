from rest_framework.routers import DefaultRouter
from .views import (WorkOrderTaskViewset,
                    WorkOrderOperationViewset,
                    WorkOrderTaskFlowItemViewset,
                    WorkOrderTaskFlowViewset,
                    WorkOrderTypeViewset,
                    WorkOrderFlowTypeViewset,
                    WorkOrderProjectViewset,
                    WorkOrderModelViewset,
                    AuditWorkOrderTaskListViewset,
                    ExecWorkOrderTaskListViewset,
                    WorkOrderTaskStatusCodeViewset,
                    WorkOrderTaskOperationStatusCodeViewset)


work_order_router = DefaultRouter()
work_order_router.register(r'workOrderTask', WorkOrderTaskViewset, base_name="workOrderTask")
work_order_router.register(r'workOrderOperation', WorkOrderOperationViewset, base_name="workOrderOperation")
work_order_router.register(r'workOrderTaskFlowItem', WorkOrderTaskFlowItemViewset, base_name="workOrderTaskFlowItem")
work_order_router.register(r'workOrderTaskFlow', WorkOrderTaskFlowViewset, base_name="workOrderTaskFlow")
work_order_router.register(r'workOrderType', WorkOrderTypeViewset, base_name="workOrderType")
work_order_router.register(r'workOrderFlowType', WorkOrderFlowTypeViewset, base_name="workOrderFlowType")
work_order_router.register(r'workOrderProject', WorkOrderProjectViewset, base_name="workOrderProject")
work_order_router.register(r'workOrderModel', WorkOrderModelViewset, base_name="workOrderModel")
work_order_router.register(r'auditWorkOrderTaskList', AuditWorkOrderTaskListViewset, base_name="auditWorkOrderTaskList")
work_order_router.register(r'execWorkOrderTaskList', ExecWorkOrderTaskListViewset, base_name="execWorkOrderTaskList")
work_order_router.register(r'workOrderTaskOperationStatusCode', WorkOrderTaskOperationStatusCodeViewset, base_name="workOrderTaskOperationStatusCode")
work_order_router.register(r'workOrderTaskStatusCode', WorkOrderTaskStatusCodeViewset, base_name="workOrderTaskStatusCode")