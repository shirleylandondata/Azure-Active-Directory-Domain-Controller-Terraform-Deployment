"""
Diagrams-as-code for the Azure AD Domain Controller Terraform lab.

Regenerates every PNG in this folder:
    pip install matplotlib
    python diagrams/generate_diagrams.py

Edit the LAB dict below if you deployed with different values
(e.g. your own `yourname` / `domain_name` from terraform.tfvars).
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

# --------------------------------------------------------------------------
# Lab values (mirror terraform.tfvars)
# --------------------------------------------------------------------------
LAB = {
    "yourname": "shirley",
    "location": "East US",
    "domain": "corp.shirley.com",
    "netbios": "CORP",
    "repo": "shirleylandondata/azure-ad-dc-terraform",
    "size": "Standard_D2ls_v7",
    "image": "2022-datacenter-g2",
}
N = LAB["yourname"]
DN = ",".join(f"DC={p}" for p in LAB["domain"].split("."))

OUT = Path(__file__).resolve().parent

# --------------------------------------------------------------------------
# Palette (matches the Lab 1 reference diagram)
# --------------------------------------------------------------------------
CARD_BG, CARD_EC = "#FAFAF8", "#D3D1C7"
TITLE, SUBTITLE = "#26215C", "#534AB7"

PURPLE = dict(ec="#534AB7", fc="#EEEDFE", tx="#3C3489", sub="#534AB7")
GREEN = dict(ec="#0F6E56", fc="#E6F0EE", tx="#085041", sub="#0F6E56")
GRAY = dict(ec="#5F5E5A", fc="#F1EFE8", tx="#2C2C2A", sub="#6B6A65")
RUST = dict(ec="#993C1D", fc="#FAECE7", tx="#712B13", sub="#993C1D")
AMBER = dict(ec="#854F0B", fc="#FAEEDA", tx="#633806", sub="#854F0B")
PINK = dict(ec="#993556", fc="#FBEAF0", tx="#72243E", sub="#993556")
TEAL = dict(ec="#0F6E56", fc="#E1F5EE", tx="#085041", sub="#0F6E56")
RG_FC, RG_TX = "#F1EEF1", "#444441"
AD_FC = "#EDF6F2"
FAINT = "#8A8984"
BODY = "#3D3D3A"
MONO = "DejaVu Sans Mono"


# --------------------------------------------------------------------------
# Drawing helpers (coordinates are "pixels", y grows downward)
# --------------------------------------------------------------------------
def canvas(w, h):
    fig = plt.figure(figsize=(w / 100, h / 100))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w)
    ax.set_ylim(h, 0)
    ax.set_aspect("equal")
    ax.axis("off")
    box(ax, 15, 15, w - 30, h - 30, CARD_BG, CARD_EC, lw=1.5, r=28, z=0)
    return fig, ax


def box(ax, x, y, w, h, fc, ec, lw=2.0, ls="-", r=12, z=1):
    p = FancyBboxPatch(
        (x + r, y + r), w - 2 * r, h - 2 * r,
        boxstyle=f"round,pad={r}", fc=fc, ec=ec, lw=lw, ls=ls, zorder=z,
    )
    ax.add_patch(p)
    return p


def container(ax, x, y, w, h, c, label, fc=None, size=17, sublabel=None):
    box(ax, x, y, w, h, fc or c["fc"], c["ec"], lw=2.5, ls=(0, (4, 3)), r=18, z=1)
    txt(ax, x + 30, y + 34, label, size, c["tx"], "bold")
    if sublabel:
        txt(ax, x + 30, y + 64, sublabel, 12.5, c["sub"])


def txt(ax, x, y, s, size=13, color=BODY, weight="normal", ha="left",
        va="center", family=None, style="normal", z=6):
    ax.text(x, y, s, fontsize=size, color=color, fontweight=weight, ha=ha,
            va=va, family=family or "DejaVu Sans", style=style, zorder=z)


def card(ax, x, y, w, h, c, title, lines=(), z=3, title_size=15):
    """Light card with bold title + subtitle lines (like Subscription/NSG cards).
    lines: list of (text, kind) where kind in {"sub", "mono", "faint", "italic"}"""
    box(ax, x, y, w, h, c["fc"], c["ec"], lw=2, r=12, z=z)
    txt(ax, x + 26, y + 34, title, title_size, c["tx"], "bold", z=z + 1)
    yy = y + 70
    for s, kind in lines:
        if kind == "mono":
            txt(ax, x + 26, yy, s, 12.5, c["sub"], family=MONO, z=z + 1)
        elif kind == "faint":
            txt(ax, x + 26, yy, s, 11.5, FAINT, z=z + 1)
        elif kind == "italic":
            txt(ax, x + 26, yy, s, 12, c["tx"], style="italic", z=z + 1)
        else:
            txt(ax, x + 26, yy, s, 13, c["sub"], z=z + 1)
        yy += 30 if kind != "faint" else 26


def header_card(ax, x, y, w, h, color, title, hh=60, fc="white", ec=None,
                title_size=16, title_family=None, z=3, center=True):
    """Card with solid colored header strip (like the VM / OU cards)."""
    ec = ec or color
    r = 12
    box(ax, x, y, w, h, color, ec, lw=0, r=r, z=z)
    box(ax, x, y + hh, w, h - hh, fc, fc, lw=0, r=r, z=z + 0.1)
    ax.add_patch(Rectangle((x, y + hh), w, h - hh - r, fc=fc, ec="none", zorder=z + 0.2))
    box(ax, x, y, w, h, "none", ec, lw=2.5, r=r, z=z + 0.3)
    txt(ax, x + (w / 2 if center else 22), y + hh / 2 + 1, title, title_size, "white",
        "bold", ha="center" if center else "left", family=title_family, z=z + 1)


def arrow(ax, x1, y1, x2, y2, color, ls="--", lw=2, label=None, lx=None, ly=None,
          label_bg=CARD_BG, z=8, rad=0.0):
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle="->,head_length=0.7,head_width=0.4", color=color,
                        lw=lw, linestyle=ls, shrinkA=0, shrinkB=0,
                        connectionstyle=f"arc3,rad={rad}"),
        zorder=z,
    )
    if label:
        ax.text(lx if lx is not None else (x1 + x2) / 2,
                ly if ly is not None else (y1 + y2) / 2, label,
                fontsize=12, color=color, ha="center", va="center", zorder=z + 1,
                bbox=dict(boxstyle="square,pad=0.45", fc=label_bg, ec="none"))


def title_block(ax, w, title, subtitle):
    txt(ax, w / 2, 62, title, 30, TITLE, "bold", ha="center")
    txt(ax, w / 2, 106, subtitle, 15.5, SUBTITLE, ha="center")


def save(fig, name):
    fig.savefig(OUT / name, dpi=114, transparent=True)
    plt.close(fig)
    print("wrote", OUT / name)


# --------------------------------------------------------------------------
# 1. Azure architecture
# --------------------------------------------------------------------------
def architecture():
    W, H = 2000, 1560
    fig, ax = canvas(W, H)
    title_block(ax, W, "Active Directory Domain Controller — Terraform on Azure",
                f"Domain: {LAB['domain']} · OS: Windows Server 2022 Gen 2 · "
                f"{LAB['size']} · Region: {LAB['location']} · IaC: Terraform")

    # Azure / RG / VNet containers
    container(ax, 70, 150, 1860, 840, PURPLE, "Microsoft Azure")
    box(ax, 105, 210, 1790, 750, RG_FC, "#5F5E5A", lw=2, ls=(0, (4, 3)), r=16, z=1.5)
    txt(ax, 133, 243, f"Resource Group: rg-ad-{N}", 15.5, RG_TX, "bold")
    txt(ax, 470 + len(N) * 9, 243, "·  tags: project = ad-lab", 12.5, FAINT)

    box(ax, 140, 280, 1115, 650, GREEN["fc"], GREEN["ec"], lw=2, ls=(0, (4, 3)), r=16, z=2)
    txt(ax, 168, 312, f"Virtual Network: vnet-ad-{N} (10.0.0.0/16)", 15.5, GREEN["tx"], "bold")
    txt(ax, 168, 340, "Subnet: snet-ad · 10.0.1.0/24", 13, GREEN["sub"])

    card(ax, 175, 368, 505, 112, RUST, f"NSG: nsg-ad-{N}",
         [("Inbound allow-rdp · TCP 3389 · priority 1000", "sub")])
    txt(ax, 201, 462, "Source: * (any) — lab only, restrict in prod", 11.5, FAINT, z=5)
    card(ax, 705, 368, 515, 112, PURPLE, f"Public IP: pip-ad-{N}",
         [("Static · Standard SKU", "sub")])
    txt(ax, 731, 462, "terraform output public_ip", 11.5, FAINT, family=MONO, z=5)

    # VM card
    header_card(ax, 175, 505, 1045, 400, GREEN["ec"], f"Virtual Machine: vm-ad-{N}", hh=62)
    rows = [
        ("Role:", "Active Directory Domain Controller (new forest)"),
        ("Hostname:", f"ad-{N}.{LAB['domain']}"),
        ("OS:", f"Windows Server 2022 Datacenter Gen 2 ({LAB['image']})"),
        ("Size:", f"{LAB['size']} (2 vCPU · Hyper-V Gen 2)"),
        ("OS Disk:", "127 GB · Premium_LRS · ReadWrite cache"),
        ("Private IP:", "10.0.1.4 (static)"),
        ("NIC:", f"nic-ad-{N} (NSG associated)"),
        ("Services:", "AD DS · DNS · RSAT management tools"),
        ("Access:", f"RDP (3389) as {LAB['netbios']}\\adadmin"),
        ("Automation:", "CustomScriptExtension “install-ad-ds” (PowerShell)"),
    ]
    for i, (k, v) in enumerate(rows):
        y = 592 + i * 31
        txt(ax, 207, y, k, 15, GREEN["tx"], "bold")
        txt(ax, 410, y, v, 15, BODY)

    # Right column
    card(ax, 1325, 280, 553, 150, PURPLE, "Terraform Workstation",
         [("Azure CLI (az login) · Terraform v1.3+", "sub"),
          ("init → plan → apply → destroy", "mono")])
    card(ax, 1325, 448, 553, 112, AMBER, "Subscription",
         [(f"Active Azure subscription · {LAB['location']}", "sub")])
    card(ax, 1325, 578, 553, 150, PINK, "Admin Workstation",
         [("Remote Desktop (RDP)", "sub"), ("→ <public_ip>:3389", "mono")])
    card(ax, 1325, 746, 553, 150, GRAY, "GitHub Repository",
         [(LAB["repo"], "faint"), ("README.md · main.tf · variables.tf · outputs.tf", "faint"),
          ("diagrams/ · screenshots/", "faint")])

    arrow(ax, 1323, 340, 1259, 355, PURPLE["ec"])
    txt(ax, 1291, 312, "apply", 11.5, PURPLE["ec"], ha="center", style="italic", z=9)
    arrow(ax, 1323, 660, 1224, 700, PINK["ec"])

    # Active Directory logical view
    container(ax, 70, 1030, 1860, 480, GREEN, f"Active Directory — {LAB['domain']}",
              fc=AD_FC)
    txt(ax, 100, 1094, f"NetBIOS: {LAB['netbios']} · single-DC forest", 13, GREEN["sub"])
    box(ax, 790, 1095, 420, 72, GREEN["ec"], GREEN["ec"], lw=0, r=10, z=3)
    txt(ax, 1000, 1131, DN, 16, "white", "bold", ha="center")
    arrow(ax, 697, 907, 1000, 1093, GREEN["ec"], label="Hosts AD DS", lx=850, ly=1003)

    ax.plot([1000, 1000], [1167, 1192], color=GREEN["ec"], lw=2.2, zorder=3)
    xs = [324, 775, 1226, 1677]
    ax.plot([xs[0], xs[-1]], [1192, 1192], color=GREEN["ec"], lw=2.2, zorder=3)
    for x in xs:
        ax.plot([x, x], [1192, 1215], color=GREEN["ec"], lw=2.2, zorder=3)

    nodes = [
        (PURPLE, "Forest & Domain",
         [f"• New forest: {LAB['domain']}", "• Forest mode: WinThreshold",
          "• Domain mode: WinThreshold"], "Install-ADDSForest"),
        (AMBER, "Authentication",
         [f"• {LAB['netbios']}\\adadmin", f"• adadmin@{LAB['domain']}",
          "• .\\adadmin (fallback only)"], "Domain creds after reboot"),
        (RUST, "DNS",
         ["• DNS Server role (-InstallDns)", "• AD-integrated zone",
          f"• Resolves {LAB['domain']}"], "Verified: Resolve-DnsName"),
        (PINK, "Recovery (DSRM)",
         ["• SafeModeAdministratorPassword", "• From var.dsrm_password",
          "• Not retrievable after deploy"], "Store in a password vault"),
    ]
    for x, (c, t, lines, it) in zip(xs, nodes):
        header_card(ax, x - 202, 1215, 405, 250, c["ec"], t, hh=50, fc=c["fc"])
        for i, s in enumerate(lines):
            txt(ax, x - 180, 1297 + i * 33, s, 14, c["tx"])
        txt(ax, x - 180, 1297 + 3 * 33 + 6, it, 13, GREEN["tx"], style="italic")

    save(fig, "architecture.png")


# --------------------------------------------------------------------------
# 2. Deployment flow
# --------------------------------------------------------------------------
def deployment_flow():
    W, H = 2000, 1560
    fig, ax = canvas(W, H)
    title_block(ax, W, "AD DC Lab — Terraform Deployment Flow",
                "terraform init → plan → apply · Custom Script Extension promotes the VM "
                "to a Domain Controller · ~10–15 min end to end")

    def lane(y, h, c, label, timing, fc=None, tx=1900):
        container(ax, 70, y, 1860, h, c, label, fc=fc)
        txt(ax, tx, y + 34, timing, 13, c["sub"], ha="right", style="italic")

    def steps(y, items, c, h=150, gap=36, mono_title=True):
        n = len(items)
        w = (1800 - gap * (n - 1)) / n
        centers = []
        for i, (t, l1, l2) in enumerate(items):
            x = 100 + i * (w + gap)
            header_card(ax, x, y, w, h, c["ec"], t, hh=48, fc="white",
                        title_size=14 if n > 4 else 15,
                        title_family=MONO if mono_title else None)
            txt(ax, x + w / 2, y + 84, l1, 12.5, c["tx"], ha="center")
            txt(ax, x + w / 2, y + 114, l2, 11.5, FAINT, ha="center")
            if i < n - 1:
                arrow(ax, x + w + 2, y + h / 2, x + w + gap - 2, y + h / 2, c["ec"], ls="-")
            centers.append(x + w / 2)
        return centers

    # Stage 1
    lane(150, 250, PURPLE, "Stage 1 · Local Workstation — Terraform CLI", "≈ 1–2 min")
    steps(215, [
        ("az login", "Authenticate to subscription", "Azure CLI"),
        ("terraform init", "Download azurerm ~> 3.0", ".terraform/ + lock file"),
        ("terraform plan", "Preview changes", "Plan: 9 to add, 0 to destroy"),
        ("terraform apply", "Create resources via ARM", "Writes terraform.tfstate"),
    ], PURPLE)

    # Stage 2
    lane(440, 250, GRAY, "Stage 2 · Azure Resource Manager — azurerm provider",
         "≈ 5–8 min", fc=RG_FC)
    res = [
        ("RG", f"rg-ad-{N}"), ("VNet", "10.0.0.0/16"), ("Subnet", "10.0.1.0/24"),
        ("Public IP", "Static · Std"), ("NSG", "allow-rdp 3389"), ("NIC", "10.0.1.4"),
        ("NIC ↔ NSG", "association"), ("Windows VM", "D2ls_v7 · Gen 2"),
        ("Extension", "install-ad-ds"),
    ]
    gap, n = 16, len(res)
    w = (1800 - gap * (n - 1)) / n
    colors = [GRAY, GREEN, GREEN, PURPLE, RUST, PURPLE, RUST, GREEN, AMBER]
    for i, ((t, s), c) in enumerate(zip(res, colors)):
        x = 100 + i * (w + gap)
        header_card(ax, x, 505, w, 150, c["ec"], t, hh=44, fc=c["fc"], title_size=13)
        txt(ax, x + w / 2, 590, s, 11.5, c["tx"], ha="center")
        txt(ax, x + w / 2, 620, f"#{i + 1}", 11, FAINT, ha="center")
        if i < n - 1:
            arrow(ax, x + w + 1, 580, x + w + gap - 1, 580, GRAY["ec"], ls="-", lw=1.5)
    ext_cx = 100 + (n - 1) * (w + gap) + w / 2

    # Stage 3
    lane(730, 250, GREEN, "Stage 3 · Inside the VM — CustomScriptExtension (PowerShell)",
         "+ 3–5 min · automatic reboot", fc=AD_FC, tx=1760)
    s3 = steps(795, [
        ("Install-WindowsFeature", "AD-Domain-Services", "-IncludeManagementTools"),
        ("Import-Module", "ADDSDeployment", "loads promotion cmdlets"),
        ("Install-ADDSForest", f"{LAB['domain']} · {LAB['netbios']}", "Forest/Domain: WinThreshold"),
        ("-InstallDns:$true", "DNS Server role + DSRM", "SafeModeAdministratorPassword"),
        ("Restart", "Automatic reboot", "Server is now a DC"),
    ], GREEN)

    # Stage 4
    lane(1020, 250, PINK, "Stage 4 · Validate — RDP + PowerShell (as Administrator)",
         "wait 5–10 min after apply before RDP", tx=1690)
    s4 = steps(1085, [
        (f"RDP", f"{LAB['netbios']}\\adadmin", f"or adadmin@{LAB['domain']}"),
        ("Get-Service NTDS", "Status: Running", "AD DS service"),
        ("Get-ADDomain", "Domain configuration", "forest & domain levels"),
        ("Get-ADDomainController", "-Filter *", f"ad-{N}.{LAB['domain']}"),
        ("Resolve-DnsName", LAB["domain"], "DNS resolves domain"),
    ], PINK)

    # Stage 5
    lane(1310, 200, GRAY, "Stage 5 · Teardown", "removes all 9 resources", fc=RG_FC)
    header_card(ax, 100, 1370, 420, 110, GRAY["ec"], "terraform destroy", hh=44,
                fc="white", title_family=MONO, title_size=15)
    txt(ax, 310, 1448, "Deletes the resource group + contents", 12.5, GRAY["tx"], ha="center")
    txt(ax, 560, 1400, "VM · OS disk · NIC · Public IP · NSG · VNet · Subnet · Extension",
        13.5, GRAY["tx"])
    txt(ax, 560, 1440, "Between sessions the VM is stopped (deallocated); disk and public IP "
        "still bill until destroy.", 12.5, FAINT, style="italic")

    # Inter-stage arrows
    arrow(ax, 1690, 367, 1690, 503, PURPLE["ec"], label="ARM API calls", lx=1690, ly=420)
    arrow(ax, ext_cx, 657, ext_cx, 793, AMBER["ec"], label="runs on VM", lx=ext_cx, ly=712)
    arrow(ax, s3[-1], 947, s3[-1], 1083, GREEN["ec"], label="DC online", lx=s3[-1], ly=1002)
    save(fig, "deployment-flow.png")


# --------------------------------------------------------------------------
# 3. Terraform resource dependency graph
# --------------------------------------------------------------------------
def resource_graph():
    W, H = 2000, 1500
    fig, ax = canvas(W, H)
    title_block(ax, W, "AD DC Lab — Terraform Resource Graph",
                "Implicit dependencies from attribute references · "
                "9 managed resources · 7 input variables · 3 outputs")

    container(ax, 70, 150, 1330, 1300, GREEN, "main.tf — managed resources", fc=AD_FC)
    cw, ch = 400, 118

    def node(cx, y, c, rtype, name, attr, cw=cw, ts=12.5):
        x = cx - cw / 2
        header_card(ax, x, y, cw, ch, c["ec"], rtype, hh=44, fc="white",
                    title_family=MONO, title_size=ts)
        txt(ax, cx, y + 70, name, 14, c["tx"], "bold", ha="center")
        txt(ax, cx, y + 97, attr, 11.5, FAINT, ha="center")
        return dict(cx=cx, top=y, bot=y + ch, l=x, r=x + cw)

    rg = node(735, 215, GRAY, "azurerm_resource_group.main", f"rg-ad-{N}",
              "location = var.location · tags")
    vnet = node(300, 420, GREEN, "azurerm_virtual_network.main", f"vnet-ad-{N}",
                "address_space 10.0.0.0/16")
    pip = node(735, 420, PURPLE, "azurerm_public_ip.main", f"pip-ad-{N}",
               "Static · Standard SKU")
    nsg = node(1170, 420, RUST, "azurerm_network_security_group.main", f"nsg-ad-{N}",
               "allow-rdp · Inbound · TCP 3389")
    snet = node(300, 625, GREEN, "azurerm_subnet.main", "snet-ad", "10.0.1.0/24")
    nic = node(517, 830, PURPLE, "azurerm_network_interface.main", f"nic-ad-{N}",
               "private IP 10.0.1.4 (Static)")
    assoc = node(1070, 1035, RUST, "…_interface_security_group_association",
                 "main", "binds NSG to NIC")
    vm = node(517, 1035, GREEN, "azurerm_windows_virtual_machine.main", f"vm-ad-{N}",
              "D2ls_v7 · 2022-datacenter-g2 · AutoLogon")
    ext = node(517, 1240, AMBER, "azurerm_virtual_machine_extension.ad_setup",
               "install-ad-ds", "CustomScriptExtension 1.10", cw=460, ts=11.5)

    E = GREEN["ec"]

    def edge(a, b, label, ax_=None, bx=None, lx=None, ly=None, c=E):
        x1 = ax_ if ax_ is not None else a["cx"]
        x2 = bx if bx is not None else b["cx"]
        arrow(ax, x1, a["bot"] + 2, x2, b["top"] - 3, c, ls="--", label=label,
              lx=lx, ly=ly, label_bg=AD_FC)

    edge(rg, vnet, "resource_group_name", ax_=620, ly=372, lx=430)
    edge(rg, pip, None)
    edge(rg, nsg, None, ax_=850)
    edge(vnet, snet, "virtual_network_name")
    edge(snet, nic, "subnet_id", bx=430)
    edge(pip, nic, "public_ip_address_id", bx=600, lx=700, ly=680)
    edge(nic, vm, "network_interface_ids")
    edge(nic, assoc, "network_interface_id", ax_=640, bx=990, lx=860, ly=985)
    edge(nsg, assoc, "network_security_group_id", ax_=1170, bx=1150, lx=1165, ly=780)
    edge(vm, ext, "virtual_machine_id")
    txt(ax, 1265, 1290, "Every resource also references\nazurerm_resource_group.main.name",
        12, FAINT, ha="right", style="italic")

    # Right column: variables / tfvars / outputs
    card(ax, 1440, 150, 490, 520, AMBER, "variables.tf", [])
    vars_ = [
        ("yourname", "string"), ("location", '"eastus"'), ("admin_password", "sensitive"),
        ("dsrm_password", "sensitive"), ("domain_name", '"corp.example.com"'),
        ("domain_netbios", '"CORP"'), ("tags", '{ project = "ad-lab" }'),
    ]
    for i, (k, v) in enumerate(vars_):
        y = 230 + i * 58
        txt(ax, 1466, y, k, 13.5, AMBER["tx"], "bold", family=MONO)
        txt(ax, 1466, y + 24, v, 12, RUST["ec"] if v == "sensitive" else FAINT,
            family=MONO, style="italic" if v == "sensitive" else "normal")

    card(ax, 1440, 700, 490, 220, GRAY, "terraform.tfvars",
         [(f'yourname = "{N}"', "mono"), (f'domain_name = "{LAB["domain"]}"', "mono"),
          ("Contains secrets → git-ignored", "faint"),
          ("Commit terraform.tfvars.example instead", "faint")])
    arrow(ax, 1685, 698, 1685, 672, GRAY["ec"], ls="-")

    card(ax, 1440, 950, 490, 250, PINK, "outputs.tf", [])
    outs = [("public_ip", "azurerm_public_ip.main.ip_address"),
            ("domain_name", "var.domain_name"), ("admin_username", '"adadmin"')]
    for i, (k, v) in enumerate(outs):
        y = 1025 + i * 56
        txt(ax, 1466, y, k, 13.5, PINK["tx"], "bold", family=MONO)
        txt(ax, 1466, y + 24, v, 11.5, FAINT, family=MONO)

    # Legend
    box(ax, 1440, 1230, 490, 220, "white", GRAY["ec"], lw=1.5, r=12, z=3)
    txt(ax, 1466, 1262, "Legend", 14, GRAY["tx"], "bold")
    leg = [(GRAY, "Resource group"), (GREEN, "Network / compute"), (PURPLE, "IP / interface"),
           (RUST, "Security"), (AMBER, "Automation")]
    for i, (c, s) in enumerate(leg):
        col, row = i % 2, i // 2
        x, y = 1466 + col * 235, 1305 + row * 40
        box(ax, x, y - 11, 34, 22, c["ec"], c["ec"], lw=0, r=4, z=4)
        txt(ax, x + 46, y, s, 12, BODY)
    ax.plot([1466, 1500], [1425, 1425], color=E, lw=2, ls="--", zorder=4)
    txt(ax, 1512, 1425, "depends on (attribute ref)", 12, BODY)

    save(fig, "terraform-resource-graph.png")


# --------------------------------------------------------------------------
# 4. Troubleshooting path (real issues hit during deployment)
# --------------------------------------------------------------------------
def troubleshooting():
    W, H = 2000, 1330
    fig, ax = canvas(W, H)
    title_block(ax, W, "AD DC Lab — Troubleshooting & State Reconciliation",
                "Issues hit during the real deployment · how each was investigated, "
                "fixed and verified")
    cols = [(RUST, "Symptom"), (PURPLE, "Investigation"), (AMBER, "Root cause"),
            (GREEN, "Fix"), (PINK, "Result")]
    issues = [
        ("Issue 1 · Azure VM SKU capacity", [
            [("terraform apply fails", "tx"), ("SkuNotAvailable", "mono"),
             ("Standard_D2s_v3 · East US", "faint")],
            [("Queried available sizes", "tx"), ("az vm list-skus", "mono"),
             ("--location eastus", "faint")],
            [("Size not offered to this", "tx"), ("subscription in region", "tx")],
            [("Switch VM size", "tx"), (f'size = "{LAB["size"]}"', "mono")],
            [("Available size selected", "tx"), ("from CLI data, not guesswork", "faint")],
        ]),
        ("Issue 2 · Hyper-V generation mismatch", [
            [("VM create fails", "tx"), ("size requires Gen 2 image", "faint")],
            [("Checked SKU capabilities", "tx"), ("HyperVGenerations", "mono"),
             ("= V2", "faint")],
            [("2022-Datacenter image", "tx"), ("is Hyper-V Gen 1", "tx")],
            [("Change image SKU", "tx"), (f'sku = "{LAB["image"]}"', "mono")],
            [("Windows Server VM", "tx"), ("deployed successfully", "faint")],
        ]),
        ("Issue 3 · Extension status “Unknown” during DC reboot", [
            [("apply reports extension", "tx"), ("status: Unknown", "mono")],
            [("Validated in Azure directly", "tx"), ("az vm extension show", "mono"),
             ("--name install-ad-ds", "faint")],
            [("Promotion reboot broke", "tx"), ("Terraform status polling", "tx")],
            [("Did NOT redeploy", "tx"), ("verify real state first", "faint")],
            [("provisioningState", "tx"), ("Succeeded", "mono")],
        ]),
        ("Issue 4 · Terraform state drift", [
            [("terraform plan wants to", "tx"), ("create install-ad-ds again", "tx")],
            [("Resource exists in Azure", "tx"), ("but not in tfstate", "faint")],
            [("Interrupted apply never", "tx"), ("recorded the extension", "tx")],
            [("terraform import", "mono"), ("…ad_setup <extension-id>", "faint")],
            [("terraform plan", "mono"), ("no longer recreates it", "faint")],
        ]),
    ]
    gap, n = 36, 5
    w = (1800 - gap * (n - 1)) / n
    for li, (label, cards) in enumerate(issues):
        y0 = 150 + li * 255
        container(ax, 70, y0, 1860, 235, GRAY, label, fc=RG_FC, size=16)
        for ci, ((c, head), lines) in enumerate(zip(cols, cards)):
            x = 100 + ci * (w + gap)
            header_card(ax, x, y0 + 60, w, 155, c["ec"], head, hh=40, fc="white",
                        title_size=13.5)
            for k, (s, kind) in enumerate(lines):
                yy = y0 + 60 + 68 + k * 28
                if kind == "mono":
                    txt(ax, x + w / 2, yy, s, 12, c["tx"], "bold", ha="center", family=MONO)
                elif kind == "faint":
                    txt(ax, x + w / 2, yy, s, 11.5, FAINT, ha="center")
                else:
                    txt(ax, x + w / 2, yy, s, 12.5, c["tx"], ha="center")
            if ci < n - 1:
                arrow(ax, x + w + 2, y0 + 137, x + w + gap - 2, y0 + 137, GRAY["ec"], ls="-")
    header_card(ax, 70, 1180, 1860, 110, GREEN["ec"], "Takeaway", hh=40, fc=AD_FC)
    txt(ax, 1000, 1255, "Validate resource state in Azure independently, then reconcile "
        "Terraform state with import instead of redeploying working infrastructure.",
        13.5, GREEN["tx"], ha="center")
    save(fig, "troubleshooting-path.png")


if __name__ == "__main__":
    architecture()
    deployment_flow()
    resource_graph()
    troubleshooting()
