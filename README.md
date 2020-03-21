# 7750-CONFGEN-19.10.R*

7750 Configuration Generator for SROS 19.10.R* (Has not been tested on any other version)

A faster, easier way to build a virtual lab configuration for the Nokia 7750s utilizing Netmiko, Jinja2 and Yaml.

This project is aimed at speeding up the configuration process of deploying a configuration on lab nodes. The driving force here is Python 3 and Netmiko to configure devices. Therefore, IP connectivity must be established before utilizing the scripts.

Ensure you have IP connectivity via the MGMT connection. All tests have been performed using EVE-NG. At this time, the code doesn't save the generated configuration to a file, it simply is aimed at deploying the configuration in real time to a running vSR.

Things to note regarding the configuration:

    The template takes advantage of a policy-statement and auto-lsp template to create a full-mesh of MPLS LSPs.
    The MPLS-LSPs are limited to Facility Fast Re-Route due to auto-lsp.
    The template includes a pw-template and leverages BGP-AD (Auto-Discovery) to auto-create MESH-SDPs across a VPLS.
    The template includes an LDP template to establish Targeted-LDP sessions.
