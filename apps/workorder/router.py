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
                    WorkOrderTaskAuditHistoryViewSet,
                    WorkOrderHistCountCheckByProductViewSet,
                    LineChartDataViewSet,
                    LineChartViewSet)


work_order_router = DefaultRouter()
work_order_router.register(r'workOrderTask', WorkOrderTaskViewset, basename="workOrderTask")
work_order_router.register(r'workOrderOperation', WorkOrderOperationViewset, basename="workOrderOperation")
work_order_router.register(r'templateWorkOrderTaskFlowItem', TemplateWorkOrderTaskFlowItemViewset, basename="templateWorkOrderTaskFlowItem")
work_order_router.register(r'templateWorkOrderTaskFlow', TemplateWorkOrderTaskFlowViewset, basename="templateWorkOrderTaskFlow")
work_order_router.register(r'templateWorkOrderType', TemplateWorkOrderTypeViewset, basename="templateWorkOrderType")
work_order_router.register(r'templateWorkOrderFlowType', TemplateWorkOrderFlowTypeViewset, basename="templateWorkOrderFlowType")
work_order_router.register(r'templateWorkOrderProject', TemplateWorkOrderProjectViewset, basename="templateWorkOrderProject")
work_order_router.register(r'templateWorkOrderModel', TemplateWorkOrderModelViewset, basename="templateWorkOrderModel")
work_order_router.register(r'auditWorkOrderTaskList', AuditWorkOrderTaskListViewset, basename="auditWorkOrderTaskList")
work_order_router.register(r'execWorkOrderTaskList', ExecWorkOrderTaskListViewset, basename="execWorkOrderTaskList")
work_order_router.register(r'workOrderTaskOperationStatusCode', WorkOrderTaskOperationStatusCodeViewset, basename="workOrderTaskOperationStatusCode")
work_order_router.register(r'workOrderTaskStatusCode', WorkOrderTaskStatusCodeViewset, basename="workOrderTaskStatusCode")
work_order_router.register(r'workOrderTaskHistory', WorkOrderTaskHistoryViewset, basename="workOrderTaskHistory")
work_order_router.register(r'workOrderHistoryCount', WorkOrderHistoryCountViewSet, basename="WorkOrderHistoryCountViewSet")
work_order_router.register(r'workOrderTaskExecHistory', WorkOrderTaskExecHistoryViewSet, basename="workOrderTaskExecHistory")
work_order_router.register(r'workOrderTaskAuditHistory', WorkOrderTaskAuditHistoryViewSet, basename="workOrderTaskAuditHistory")
work_order_router.register(r'workOrderHistCountCheckByProduct', WorkOrderHistCountCheckByProductViewSet, basename="workOrderHistCountCheckByProduct")
work_order_router.register(r'lineChartData', LineChartDataViewSet, basename="lineChartData")
work_order_router.register(r'lineChart', LineChartViewSet, basename="lineChart")