import subprocess


class CheckPermission:
    """
    This class gets a name of a permission rule and check if it exists.
    """

    def __init__(self, permission_name):
        self.NAME_OF_PERMISSION = permission_name

    def get_all_rules(self):
        """
        This all rules with the permission name
        :return:
        """

        try:
            return subprocess.check_output('netsh advfirewall firewall show rule name=%s' % self.NAME_OF_PERMISSION, shell=True)
        except subprocess.CalledProcessError:
            return b""

    def check(self):
        """
        Return True if the rule exists and False otherwise.
        :return:
        """

        return self.get_all_rules() == b""
