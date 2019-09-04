from rest_framework.routers import DefaultRouter
from .views import (WorkOrderTaskViewset,
                    WorkOrderOperationViewset,
                    WorkOrderTaskFlowItemViewset,
                    WorkOrderTaskFlowViewset,
                    WorkOrderTypeViewset,
                    WorkOrderFlowTypeViewset,
                    WorkOrderProjectViewset,
                    WorkOrderModelViewset)


work_order_router = DefaultRouter()
work_order_router.register(r'workOrderTask', WorkOrderTaskViewset, base_name="workOrderTask")
work_order_router.register(r'workOrderOperation', WorkOrderOperationViewset, base_name="workOrderOperation")
work_order_router.register(r'workOrderTaskFlowItem', WorkOrderTaskFlowItemViewset, base_name="workOrderTaskFlowItem")
work_order_router.register(r'workOrderTaskFlow', WorkOrderTaskFlowViewset, base_name="workOrderTaskFlow")
work_order_router.register(r'workOrderType', WorkOrderTypeViewset, base_name="workOrderType")
work_order_router.register(r'WorkOrderFlowType', WorkOrderFlowTypeViewset, base_name="WorkOrderFlowType")
work_order_router.register(r'WorkOrderProject', WorkOrderProjectViewset, base_name="WorkOrderProject")
work_order_router.register(r'WorkOrderModel', WorkOrderModelViewset, base_name="WorkOrderModel")