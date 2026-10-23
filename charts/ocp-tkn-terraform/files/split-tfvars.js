/*
This NodeJS function will take a JSON structure from a Kubernetes Secret,
and convert it to a Terraform tfvars file that looks like:

apiOwnersGithubOrg {
    access_token = ""
    client_id = ""
}
*/
const fs = require("fs")

// Usage: node split-tfvars.js input.json output.tfvars [base64|utf-8]
const encoding = process.argv[4] || "base64"
if (!["base64", "utf-8"].includes(encoding)) {
  console.error("Encoding must be base64 or utf-8")
  process.exit(1)
}
// Escape Terraform template sequences as literal data as well as JSON strings.
const quote = (value) => JSON.stringify(value.replace(/\$\{/g, () => "$${").replace(/%\{/g, "%%{"))
const decode = (value) => {
  if (typeof value !== "string") throw new Error("tfvars data values must be strings")
  return Buffer.from(value, encoding).toString("utf8").trim()
}

fs.readFile(process.argv[2], function (err, data) {
  if (err) {
    console.log(err)
    process.exit(1)
  }
  let outputFile = ""
  const out = (msg) => (outputFile = outputFile + msg + "\n")

  let theRoot = ""
  let config = JSON.parse(data)["data"]
  if (!config || typeof config !== "object" || Array.isArray(config)) {
    console.error("Input must contain a data object")
    process.exit(1)
  }
  Object.keys(config)
    .sort()
    .forEach((k) => {
      const keyParts = k.split(".")
      if (keyParts.length > 2 || keyParts.some(part => !/^[A-Za-z_][A-Za-z0-9_-]*$/.test(part))) {
        throw new Error("Unsupported tfvars key")
      }
      if (keyParts.length == 1) {
        if (theRoot != "") {
          out("}\n")
          theRoot = ""
        }
        out(
          k +
            ' = ' + quote(decode(config[k])) + '\n'
        )
      } else if (theRoot != keyParts[0]) {
        if (theRoot != "") {
          out("}\n")
        }
        theRoot = keyParts[0]
        out(theRoot + " = {")
        out(
          "  " +
            keyParts[1].padEnd(20) +
            " = " +
            quote(decode(config[k])) +
            ""
        )
      } else {
        out(
          "  " +
            keyParts[1].padEnd(20) +
            " = " +
            quote(decode(config[k])) +
            ""
        )
      }
    })

  if (theRoot !== "") out("}\n")

  fs.writeFile(process.argv[3], outputFile, { mode: 0o600 }, function (err) {
    if (err) {
      console.log(err)
      process.exit(1)
    }
    console.log("tfvars written to " + process.argv[3])
  })
})
