# -*- mode: ruby -*-
# vi: set ft=ruby :

require 'etc'
require 'pathname'

Vagrant.configure("2") do |config|
    # define synced folders
    config.vm.synced_folder ".", "/home/vagrant/pwc-bin-packing"

    config.vm.define "pbp" do |pbp|
        # define virtualization provider
        pbp.vm.provider "virtualbox"
        # define box
        pbp.vm.box = "ubuntu/trusty64"

        config.vm.provider "virtualbox" do |v|
            # define RAM in MBs
            v.memory = 1024
            # define number of vCPUs
            v.cpus = 1
        end
    end

    # forward SSH agent
    config.ssh.forward_agent = true
    config.ssh.insert_key = false

    config.vm.network :forwarded_port, guest: 22, host: 2402, id: "ssh", auto_correct: false

    # provision with Ansible
    config.vm.provision :ansible do |ansible|
        ansible.playbook = "package-pwc-bin-packing.yaml"

        if ENV['ANSIBLE_TAGS'] != ""
            ansible.tags = ENV['ANSIBLE_TAGS']
        end

        ansible.extra_vars = {
            "app_pwc_bin_packing"=> {is_vagrant: true},
        }
    end
end
