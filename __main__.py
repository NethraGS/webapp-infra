import pulumi
from pulumi_azure_native import resources, web

config = pulumi.Config()

env = config.get("env") or "dev"

# Resource Group
rg = resources.ResourceGroup(f"rg-{env}")

# App Service Plan
plan = web.AppServicePlan(
    f"plan-{env}",
    resource_group_name=rg.name,
    sku={
        "name": "B1" if env == "dev" else "P1v2",
        "tier": "Basic" if env == "dev" else "PremiumV2"
    }
)

# Web App
app = web.WebApp(
    f"app-{env}",
    resource_group_name=rg.name,
    server_farm_id=plan.id,
)

pulumi.export("url", app.default_host_name)
