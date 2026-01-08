# Directory needs to be created manually in beforehand
MOUNT_POINT="/Volumes/FritzNAS"
USER=""
PASSWORD=""
SERVER="//$USER:$PASSWORD@192.168.178.1"
SHARE="keller"
LOCKFILE="/tmp/mount-fritznas.lock"
LOGFILE="$HOME/Library/Logs/fritznas-sync.log"

exec >>"$LOGFILE" 2>&1

echo "===== $(date) ====="

if [[ -e "$LOCKFILE" ]]; then
  echo "Script already running. Exit."
  exit 0
fi
touch "$LOCKFILE"
trap "rm -f $LOCKFILE" EXIT

echo "Mount FritzNAS..."

if ! mount | grep -q "$MOUNT_POINT"; then
  /sbin/mount_smbfs "$SERVER/$SHARE" "$MOUNT_POINT"
fi

echo "Waiting for mount..."
for i in {1..30}; do
  mount | grep -q "$MOUNT_POINT" && break
  sleep 2
done

if ! mount | grep -q "$MOUNT_POINT"; then
  echo "ERROR: FritzNAS not mounted"
  exit 1
fi

echo "FritzNAS mounted successfully"

echo 'Synchronisiere FritzNAS -> MacBook'
rsync -aruvz --exclude={Studium,Schule} "$MOUNT_POINT/WIEMES/Dateisicherung/Dokumente/" /Volumes/Daten/Dokumente/
rsync -aruvz "$MOUNT_POINT/WIEMES/Dateisicherung/Bilder/" /Volumes/Daten/Bilder/

echo 'Synchronisiere MacBook -> FritzNAS'
rsync -aruvz --exclude={Studium,Schule} /Volumes/Daten/Dokumente/ "$MOUNT_POINT/WIEMES/Dateisicherung/Dokumente/"
rsync -aruvz /Volumes/Daten/Bilder/ "$MOUNT_POINT/WIEMES/Dateisicherung/Bilder/"

echo "Sync finished successfully"