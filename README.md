# BCGOV Helm Charts Repo

This helm chart repo is available for use on the command line at http://bcgov.github.io/helm-charts

It uses: https://github.com/helm/chart-releaser

Run `./package.sh` to push new released artifacts to Github.

Note: `CR_TOKEN` is a Github Personal Access Token with `repo` scope.

## ⚠️ Helm Chart Usage and Responsibilities

Each **development team** is **accountable** for the resources they deploy within their own namespaces.

The original purpose of this repository was to serve as a **centralized location** for commonly used **Helm charts**, supporting **community collaboration**. However, ongoing **maintenance and updates** to these charts were always intended to be a **shared community effort**—not the sole responsibility of the **Platform Services team**.

As with any **publicly available resource**—even those shared by **trusted sources**—it's essential to **review and validate configurations** before use. This helps mitigate potential risks associated with **outdated or insecure components**.

> 🛡️ **Security Alert**  
> Microsoft recently issued a warning about the risks of using **default Helm charts** without proper vetting. These charts often prioritize **ease of use over security**, potentially exposing Kubernetes applications to **misconfigurations**, **data leaks**, or **unauthorized access**.  
> 🔗 [Read the full article](https://thehackernews.com/2025/05/microsoft-warns-default-helm-charts-for.html)

Please note that the **Platform Services team does not monitor or update** the container images or configuration values you choose to deploy.

For **security assessments**, your **Ministry Security team** can assist in identifying vulnerabilities in images or configurations using tools such as **ACS** or **Sysdig**.

