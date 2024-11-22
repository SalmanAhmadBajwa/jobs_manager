from datetime import datetime, timedelta

from django.db.models import Sum
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework.views import APIView

from workflow.models import BillLineItem, InvoiceLineItem


class ReportCompanyProfitAndLoss(APIView):
    def get(self, request):
        # Input parameters
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        compare_periods = int(request.query_params.get("compare", 0))

        # Generate date ranges
        date_ranges = []
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        for i in range(compare_periods + 1):
            period_start = start_date - timedelta(days=30 * i)
            period_end = end_date - timedelta(days=30 * i)
            date_ranges.append((period_start, period_end))

        # Aggregate data
        report = {
            "periods": [],
            "income": {},
            "cost_of_sales": {},
            "expenses": {},
            "unclassified": {},
            "totals": {"gross_profit": []},
        }

        for i, (period_start, period_end) in enumerate(reversed(date_ranges)):
            report["periods"].append(period_start.strftime("%b %Y"))

            # Invoices aggregation
            invoices = (
                InvoiceLineItem.objects.filter(
                    invoice__date__range=[period_start, period_end]
                )
                .values("account__account_name", "account__account_type")
                .annotate(total=Sum("line_amount"))
            )

            # Bills aggregation
            bills = (
                BillLineItem.objects.filter(
                    bill__date__range=[period_start, period_end]
                )
                .values("account__account_name", "account__account_type")
                .annotate(total=Sum("line_amount"))
            )

            # Categorize
            for invoice in invoices:
                account_type = invoice.get("account__account_type")
                account_name = invoice["account__account_name"]
                total = invoice["total"]

                if account_type == "AccountType.REVENUE":
                    report["income"].setdefault(account_name, []).append(total)
                elif not account_type:  # Handle missing account type
                    report["unclassified"].setdefault("Invoices", []).append(
                        {"name": account_name, "total": total}
                    )
                else:
                    report["unexpected"].setdefault("Invoices", []).append(
                        {"name": account_name, "type": account_type, "total": total}
                    )

            for bill in bills:
                account_type = bill.get("account__account_type")
                account_name = bill["account__account_name"]
                total = bill["total"]

                if account_type == "AccountType.DIRECTCOSTS":
                    report["cost_of_sales"].setdefault(account_name, []).append(total)
                elif account_type in ["AccountType.EXPENSE", "AccountType.OVERHEADS"]:
                    report["expenses"].setdefault(account_name, []).append(total)
                elif not account_type:  # Handle missing account type
                    report["unclassified"].setdefault("Bills", []).append(
                        {"name": account_name, "total": total}
                    )
                else:
                    report["unexpected"].setdefault("Bills", []).append(
                        {"name": account_name, "type": account_type, "total": total}
                    )

            # Gross Profit
            total_income = sum(
                report["income"].get(account, [0])[i] for account in report["income"]
            )
            total_cogs = sum(
                report["cost_of_sales"].get(account, [0])[i]
                for account in report["cost_of_sales"]
            )
            gross_profit = total_income - total_cogs
            report["totals"]["gross_profit"].append(gross_profit)

        return Response(report)


class CompanyProfitAndLossView(TemplateView):
    template_name = "reports/report_company_profit_and_loss.html"
