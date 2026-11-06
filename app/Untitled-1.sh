{
  echo "L03 report"
  date -u +%Y-%m-%dT%H:%M:%SZ
  echo "--- plan"
  az appservice plan show --resource-group rg-cloudnotes --name plan-cloudnotes-Pszy15 --query "{sku:sku.name, tier:sku.tier, linux:reserved, region:location}" -o table
  echo "--- web app"
  az webapp show --resource-group rg-cloudnotes --name app-cloudnotes-Pszy15 --query "{state:state, host:defaultHostName, httpsOnly:httpsOnly, runtime:siteConfig.linuxFxVersion}" -o table
  echo "--- resources"
  az resource list --resource-group rg-cloudnotes --query "[].{name:name, type:type}" -o table
  echo "--- app settings"
  az webapp config appsettings list --resource-group rg-cloudnotes --name app-cloudnotes-Pszy15 --query "[].{name:name, value:value}" -o table
  echo "--- health over https"
  curl -sS --max-time 60 https://app-cloudnotes-Pszy15.azurewebsites.net/health
  echo
  echo "--- http request"
  curl -s -o /dev/null -w "%{http_code} %{redirect_url}\n" http://app-cloudnotes-Pszy15.azurewebsites.net/health
  echo "--- B1 monthly price"
  echo "B1=<KOSZT_B1> USD"
} > ~/l03-report.txt