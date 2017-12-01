<#--

    Copyright 2017 XEBIALABS

    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

-->
unzip ${previousDeployed.file.path} -d .
<#if previousDeployed.serviceNames?has_content>
  <#list previousDeployed.serviceNames as serviceName>
    <@compress single_line=true>
${previousDeployed.container.cliPath}
<#if previousDeployed.container.url??>--url ${previousDeployed.container.url} </#if>
<#if previousDeployed.container.accessKey??>--access-key ${previousDeployed.container.accessKey} </#if>
<#if previousDeployed.container.secretKey??>--secret-key ${previousDeployed.container.secretKey} </#if>
<#if previousDeployed.container.config??>--config ${previousDeployed.container.config} </#if>
<#if previousDeployed.wait>--wait </#if>
<#if previousDeployed.waitTimeout??>--wait-timeout ${previousDeployed.waitTimeout} </#if>
<#if previousDeployed.waitState??>--wait-state ${previousDeployed.waitState} </#if>
up -d --rollback --stack ${previousDeployed.name} ${serviceName}
    </@compress>

  </#list>
<#else>
<@compress single_line=true>
${previousDeployed.container.cliPath}
<#if previousDeployed.container.url??>--url ${previousDeployed.container.url} </#if>
<#if previousDeployed.container.accessKey??>--access-key ${previousDeployed.container.accessKey} </#if>
<#if previousDeployed.container.secretKey??>--secret-key ${previousDeployed.container.secretKey} </#if>
<#if previousDeployed.container.config??>--config ${previousDeployed.container.config} </#if>
<#if previousDeployed.wait>--wait </#if>
<#if previousDeployed.waitTimeout??>--wait-timeout ${previousDeployed.waitTimeout} </#if>
<#if previousDeployed.waitState??>--wait-state ${previousDeployed.waitState} </#if>
up -d --rollback --stack ${previousDeployed.name}
</@compress>

</#if>
