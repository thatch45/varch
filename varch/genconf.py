'''
The genconf module is where the code the generates configurations for specific
hypervisors is found.
This module needs to support qemu-kvm, qemu, libvirt and open nebula
'''

import os
import stat
import uuid
import random

def gen_mac(form='qemu'):
    '''
    Generates a mac addr, form can be xen, rand or qemu, qemu is default
    '''
    src = ['1','2','3','4','5','6','7','8','9','0','A','B','C','D','E','F']
    mac = ''
    if form == 'xen':
        mac = '00:16:3E:'
    if form == 'qemu':
        mac = '52:54:00:'
    while len(mac) < 18:
        if len(mac) < 3:
            mac = random.choice(src) + random.choice(src) + ':'
        if mac.endswith(':'):
            mac += random.choice(src) + random.choice(src) + ':'
    return mac[:-1]


class GenConf:
    '''
    Generates the desired configuration files and places them in the same
    directory as the image.
    '''
    def __init__(self, opts):
        self.opts = opts
        self._dir = os.path.dirname(self.opts['image'])

    def gen_kvm(self):
        '''
        Generates a shell script to start qemu-kvm images.
        '''
        fn_ = os.path.join(self._dir, self.opts['image'] + '-kvm.sh')
        lines = [
            'qemu-kvm -drive file=' + self.opts['image'] + ',if=virtio,'\
            + 'boot=on -m 512\n',
            ]
        open(fn_, 'w+').writelines(lines)
        os.chmod(fn_, 0755)

    def gen_libvirt(self):
        '''
        Generates a libvirt configuration file
        '''
        fn_ = os.path.join(self._dir, self.opts['image'] + '-virt.xml')
        lines = [
            "<domain type='kvm'>\n",
            "  <name>" + os.path.basename(self.opts['image']) + "</name>\n",
            "  <uuid>" + uuid.uuid4().__str__() + "</uuid>\n",
            "  <memory>524288</memory>\n",
            "  <currentMemory>524288</currentMemory>\n",
            "  <vcpu>1</vcpu>\n",
            "  <os>\n",
            "    <type arch='x86_64' machine='pc-0.12'>hvm</type>\n",
            "    <boot dev='hd'/>\n",
            "  </os>\n",
            "  <features>\n",
            "    <acpi/>\n",
            "    <apic/>\n",
            "    <pae/>\n",
            "  </features>\n",
            "  <clock offset='utc'/>\n",
            "  <on_poweroff>destroy</on_poweroff>\n",
            "  <on_reboot>restart</on_reboot>\n",
            "  <on_crash>restart</on_crash>\n",
            "  <devices>\n",
            "    <emulator>/usr/bin/qemu-kvm</emulator>\n",
            "    <disk type='file' device='disk'>\n",
            "      <driver name='qemu' type='raw'/>\n",
            "      <source file='" + self.opts['image'] + "'/>\n",
            "      <target dev='vda' bus='virtio'/>\n",
            "      <address type='pci' domain='0x0000' bus='0x00' slot='0x04' function='0x0'/>\n",
            "    </disk>\n",
            "    <interface type='network'>\n",
            "      <mac address='" + gen_mac() + "'/>\n",
            "      <source network='default'/>\n",
            "      <model type='virtio'/>\n",
            "      <address type='pci' domain='0x0000' bus='0x00' slot='0x06' function='0x0'/>\n",
            "    </interface>\n",
            "    <serial type='pty'>\n",
            "      <target port='0'/>\n",
            "    </serial>\n",
            "    <console type='pty'>\n",
            "      <target type='serial' port='0'/>\n",
            "    </console>\n",
            "    <input type='mouse' bus='ps2'/>\n",
            "    <graphics type='vnc' port='-1' autoport='yes'/>\n",
            "    <sound model='ac97'>\n",
            "      <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>\n",
            "    </sound>\n",
            "    <video>\n",
            "      <model type='cirrus' vram='9216' heads='1'/>\n",
            "      <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x0'/>\n",
            "    </video>\n",
            "    <memballoon model='virtio'>\n",
            "      <address type='pci' domain='0x0000' bus='0x00' slot='0x05' function='0x0'/>\n",
            "    </memballoon>\n",
            "  </devices>\n",
            "</domain>\n",
            ]
        open(fn_, 'w+').writelines(lines)

    def gen_open_nebula(self):
        '''
        Generates a open nebula configuration file, well, not yet :)
        '''
        fn_ = os.path.join(self._dir, self.opts['image'] + '.one')
        
