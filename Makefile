
config_boot:
	~/rasp_pi_chip_test/shell/boot_config.sh
do_update:
	~/rasp_pi_chip_test/shell/update_pi.sh

update: do_update config_boot

gpib:
	~/rasp_pi_chip_test/shell/install.sh


