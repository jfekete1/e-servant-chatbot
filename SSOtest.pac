function FindProxyForURL(url, host) {


/* */
//DEFAULT PAC
/* */
/* Local. This entry needs to be above the pxy declaration for Java to parse it properly*/
if (isPlainHostName(host) ||
shExpMatch(host,"*.xom.com") ||
shExpMatch(host,"*.xom.local") ||
shExpMatch(host,"*.local")) { /* CRQ000000519210 */
return "DIRECT";
}
/* */
var pxy = "PROXY cn-1998263328-6-nx12468.ibosscloud.com:80; PROXY cn-1998263339-38-nx12469.ibosscloud.com:80";
/* */
//FOR PAC FILE EDITOR - DO NOT REMOVE THIS
//FOR PAC FILE EDITOR - DO NOT REMOVE THIS
// SWG PAC Files
// SWG PAC Files and reporters (error and blockpages)
if (shExpMatch(host, "datadoghq.com") || shExpMatch(host, "*.datadoghq.com")) {
return "PROXY cn-1998263328-6-nx12468.ibosscloud.com:80; PROXY cn-1998263339-38-nx12469.ibosscloud.com:80";
}

/* */
//Default PAC v2

return "DIRECT";
}
