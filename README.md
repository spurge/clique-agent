Clique Agent
============

A KVM agent that:

* Listens on a RabbitMQ task queue for virtualization jobs, which could be
    - setup some new machine
    - destroy some machine
* Monitors health status for it's local machines
* Reports with stats to RabbitMQ

Dependencies
------------

* [libvirt](https://libvirt.org/)
* [qemu](http://wiki.qemu.org/Main_Page)
* Python >= 3.4
* ~~[python-kvm](https://github.com/fmenabe/python-kvm/)~~
* [python-libvirt](https://www.libvirt.org/python.html)

Setup
-----

### Libvirt

Run the libvirt daemon

### Polkit access

Ensure you have a passwordless manage access (_org.libvirt.unix.manage_)

For example, if you want to use the `wheel` group:

```
polkit.addRule(function(action, subject) {
    if ((action.id == "org.libvirt.unix.manage" ||
         action.id == "org.libvirt.unix.monitor") &&
        subject.isInGroup("wheel"))
    {
        return polkit.Result.YES;
    }
});
```
