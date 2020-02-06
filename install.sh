# ###############################################################
# Trade Telegraph CLI Installation Script
# ###############################################################

# ---------------------------------------------------------------
# SECTION: HELPER VARIABLES
# ---------------------------------------------------------------

# GitHub repo.
declare _REPO_NAME=stests
declare _REPO=https://github.com/CasperLabs/$_REPO_NAME.git

# OS types.
declare _OS_LINUX="linux"
declare _OS_LINUX_REDHAT="$_OS_LINUX-redhat"
declare _OS_LINUX_SUSE="$_OS_LINUX-suse"
declare _OS_LINUX_ARCH="$_OS_LINUX-arch"
declare _OS_LINUX_DEBIAN="$_OS_LINUX-debian"
declare _OS_MACOSX="macosx"
declare _OS_UNKNOWN="unknown"

# Root directory.
declare _HOME=$HOME/.casperlabs-stests

# ---------------------------------------------------------------
# SECTION: HELPER FUNCTIONS
# ---------------------------------------------------------------

# Wraps standard echo.
function log()
{
	declare now=`date +%Y-%m-%dT%H:%M:%S`
	echo -e $now" [INFO] :: STESTS > "$1
}

# Outputs a line to split up logging.
function log_banner()
{
	echo "-------------------------------------------------------------------------------"
}

# Returns OS type.
function get_os()
{
	if [[ "$OSTYPE" == "linux-gnu" ]]; then
		if [ -f /etc/redhat-release ]; then
			echo $_OS_LINUX_REDHAT
		elif [ -f /etc/SuSE-release ]; then
			echo $_OS_LINUX_SUSE
		elif [ -f /etc/arch-release ]; then
			echo $_OS_LINUX_ARCH
		elif [ -f /etc/debian_version ]; then
			echo $_OS_LINUX_DEBIAN
		fi
	elif [[ "$OSTYPE" == "darwin"* ]]; then
		echo $_OS_MACOSX
	else
		echo $_OS_UNKNOWN
	fi
}

# Returns directory in which application will be installed.
function get_install_dir()
{
	declare os_type="$(get_os)"
	if [[ $os_type == $_OS_LINUX* ]]; then
        echo "/opt/casperlabs"
	elif [[ $os_type == $_OS_MACOSX ]]; then
		echo "$HOME/casperlabs"
	else
		echo "$HOME/casperlabs"
	fi
}

# Returns directory in which repo will be installed.
function get_repo_dir()
{
	echo "$(get_install_dir)/$_REPO_NAME"
}

# Returns file path of bash terminal session initiliser.
function get_bashrc_filepath()
{
	declare os_type="$(get_os)"
	if [[ $os_type == $_OS_MACOSX ]]; then
		echo "$HOME/.bash_profile"
	else
		echo "$HOME/.bashrc"
	fi
}

# Wraps pushd command to suppress stdout.
function pushd () {
    command pushd "$@" > /dev/null
}

# Wraps popd command to suppress stdout.
function popd () {
    command popd "$@" > /dev/null
}

# Reset terminal.
function tidyup()
{
	# Unset helper vars.
	unset _REPO
	unset _OS_LINUX
	unset _OS_LINUX_REDHAT
	unset _OS_LINUX_SUSE
	unset _OS_LINUX_ARCH
	unset _OS_LINUX_DEBIAN
	unset _OS_MACOSX
	unset _OS_UNKNOWN
}

# Notify user upon installation.
function notify()
{
	log_banner
	echo "1. stests has been successfully installed."
	echo ""
	echo "2. Register a network:"
	echo "      stests-set-network loc1
	echo ""
	echo "2. Register a node:"
	echo "      stests-set-node loc1:1 localhost:40400 full
	echo ""
	echo "3. Run stests worker processes:"
	echo "      stests-workers-run
	echo ""
	echo "4. Run stests workload generator:"
	echo "      stests-wg-100 --network loc1 --run 1 --user-accounts 100
	log_banner
}

# ---------------------------------------------------------------
# SECTION: VERIFY FUNCTIONS
# ---------------------------------------------------------------

# Verify installation can proceeed.
function verify {
	log_banner
	log 'verifying system:'

	verify_previous
	verify_prequisites
}

# Verify pre-requisites.
function verify_prequisites {
	log '... prequisites'

	# Git.
	command -v git >/dev/null 2>&1 || { echo >&2 "Please install git. https://www.atlassian.com/git/tutorials/install-git"; exit 1; }
}

# Verify previous installation.
function verify_previous {
	log '... previous installation'

	declare repo_dir="$(get_repo_dir)"
	if [ -d $repo_dir ]; then
		log "... stests IS ALREADY INSTALLED !"
		log "... to update the stests stack run:"
		log "...     stests-stack-update"
		log_banner
		exit 1
	fi
}

# ---------------------------------------------------------------
# SECTION: INSTALL FUNCTIONS
# ---------------------------------------------------------------

# Install entry point.
function install()
{
	log_banner
	log 'installing:'

	install_repo
	install_activator
}

# Install repo.
function install_repo()
{
	log '... repo'

	declare install_dir="$(get_install_dir)"
	mkdir -p $install_dir
	pushd $install_dir
	git clone -q $_REPO
	popd
}

# Install shell activator.
function install_activator()
{
	log '... environment activator'

	declare repo_dir="$(get_repo_dir)"
	declare bashrc_file="$(get_bashrc_filepath)"

	cat >> $bashrc_file <<- EOM

	# ----------------------------------------------------------------------
	# CASPERLABS - STESTS - CLI
	# ----------------------------------------------------------------------

	source ${repo_dir}/activate

	EOM

	source $bashrc_file
}

# ---------------------------------------------------------------
# SECTION: MAIN ENTRY POINT
# ---------------------------------------------------------------

# Main entry point.
function main()
{
	verify
	install
	tidyup
	notify
}

main