import os
import time
from typing import Optional

# Try importing Azure SDKs; if missing, we'll fall back to simulation mode.
try:
    from azure.identity import AzureCliCredential
    from azure.mgmt.compute import ComputeManagementClient
    AZURE_SDK_AVAILABLE = True
except Exception:
    AZURE_SDK_AVAILABLE = False


class ResourceOptimizer:
    """Resource optimizer that recommends or applies VM optimizations.

    Behaviour:
    - If Azure SDKs and credentials are available, it will use AzureCliCredential
      and ComputeManagementClient to query and (optionally) modify VM size or
      perform restarts.
    - If not available, the class runs in simulation mode and returns
      recommended actions without making changes.

    Configuration via environment variables (use your .env):
    - AZURESUBSCRIPTIONID: subscription id
    - AZURERESOURCEGROUP: resource group
    - AZURERESOURCENAME: VM name (resource name)
    - OPTIMIZER_DRY_RUN: if set to '1' (default), do not apply changes — just simulate
    """

    def __init__(self, subscription: Optional[str] = None, rg: Optional[str] = None, vm_name: Optional[str] = None, dry_run: Optional[bool] = None):
        self.subscription = subscription or os.getenv("AZURESUBSCRIPTIONID", "")
        self.rg = rg or os.getenv("AZURERESOURCEGROUP", "")
        self.vm_name = vm_name or os.getenv("AZURERESOURCENAME", "")
        if dry_run is None:
            self.dry_run = os.getenv("OPTIMIZER_DRY_RUN", "1") != "0"
        else:
            self.dry_run = dry_run

        self.client = None
        if AZURE_SDK_AVAILABLE:
            try:
                cred = AzureCliCredential()
                self.client = ComputeManagementClient(cred, self.subscription)
            except Exception as e:
                print("Warning: could not initialize ComputeManagementClient; running in simulation mode.", e)
                self.client = None

    def get_vm(self):
        """Return VM model/dict. In simulation mode returns a fake sample."""
        if not self.client:
            # Simulation sample
            return {
                "name": self.vm_name or "sample-vm",
                "vm_size": "Standard_D4s_v3",
                "os_disk_size_gb": 128,
                "cpu_cores": 4,
                "memory_gb": 16,
                "power_state": "running",
            }

        # Live mode: query compute client
        try:
            vm = self.client.virtual_machines.get(self.rg, self.vm_name)
            # We intentionally avoid deep serialization; provide common fields
            hardware_profile = getattr(vm, "hardware_profile", None)
            storage_profile = getattr(vm, "storage_profile", None)
            return {
                "name": getattr(vm, "name", self.vm_name),
                "vm_size": getattr(hardware_profile, "vm_size", None),
                "os_disk_size_gb": getattr(storage_profile, "os_disk", None) and getattr(storage_profile.os_disk, "disk_size_gb", None),
                "power_state": self._get_power_state(),
            }
        except Exception as e:
            print("Error fetching VM (running in simulation):", e)
            return self.get_vm()

    def _get_power_state(self):
        """Attempt to read power state using instance view."""
        if not self.client:
            return "running"
        try:
            iv = self.client.virtual_machines.instance_view(self.rg, self.vm_name)
            states = [s.code for s in getattr(iv, "statuses", []) if s.code]
            # statuses include codes like PowerState/running
            for s in states:
                if s.lower().startswith("powerstate/"):
                    return s.split("/", 1)[1]
            return ",".join(states)
        except Exception:
            return "unknown"

    def recommend_action(self, metric_name: str, value: float):
        """Return a recommendation based on metric name and value."""
        # Simple, rule-based recommendations. Extend with ML or heuristics later.
        if "cpu" in metric_name.lower():
            if value > 80:
                return {"action": "recommend_resize", "reason": f"High CPU {value}%"}
            elif value > 60:
                return {"action": "recommend_restart", "reason": f"Moderate CPU {value}%"}
            else:
                return {"action": "no_action", "reason": f"CPU normal {value}%"}
        if "memory" in metric_name.lower():
            if value < 1e9:
                return {"action": "recommend_resize", "reason": f"Low memory {value} bytes"}
            else:
                return {"action": "no_action", "reason": f"Memory normal {value} bytes"}
        if "disk" in metric_name.lower():
            if value > 5e7:
                return {"action": "recommend_cleanup", "reason": f"High disk I/O {value}"}
            else:
                return {"action": "no_action", "reason": f"Disk I/O normal {value}"}
        return {"action": "unknown_metric", "reason": "No rule for this metric"}

    def apply_action(self, recommendation: dict):
        """Apply or simulate the recommended action.

        Supported actions (simulation-first):
        - recommend_resize: suggest a VM size and optionally perform resize (live only)
        - recommend_restart: restart the VM (live only)
        - recommend_cleanup: log cleanup recommendation
        """
        action = recommendation.get("action")
        reason = recommendation.get("reason")
        vm = self.get_vm()

        # Default recommendation messages
        if action == "no_action":
            return {"status": "ok", "message": reason}

        if action == "recommend_cleanup":
            msg = f"Recommend disk cleanup on {vm['name']}: {reason}"
            print(msg)
            return {"status": "recommended", "message": msg}

        if action == "recommend_restart":
            msg = f"Recommend restarting VM {vm['name']}: {reason}"
            print(msg)
            if self.dry_run or not self.client:
                return {"status": "simulated", "message": msg}
            try:
                async_op = self.client.virtual_machines.begin_restart(self.rg, self.vm_name)
                async_op.wait()
                return {"status": "applied", "message": msg}
            except Exception as e:
                return {"status": "error", "message": str(e)}

        if action == "recommend_resize":
            # Simple mapping for demonstration. A real implementation should
            # lookup available sizes and pick one based on metrics/cost.
            target_size = "Standard_D8s_v3"
            msg = f"Recommend resizing VM {vm['name']} to {target_size}: {reason}"
            print(msg)
            if self.dry_run or not self.client:
                return {"status": "simulated", "message": msg}
            try:
                # In Azure, changing VM size requires update of hardware_profile
                vm_model = self.client.virtual_machines.get(self.rg, self.vm_name)
                vm_model.hardware_profile.vm_size = target_size
                async_op = self.client.virtual_machines.begin_create_or_update(self.rg, self.vm_name, vm_model)
                async_op.wait()
                return {"status": "applied", "message": msg}
            except Exception as e:
                return {"status": "error", "message": str(e)}

        return {"status": "unknown_action", "message": f"Action {action} not supported"}


if __name__ == "__main__":
    opt = ResourceOptimizer()
    vm = opt.get_vm()
    print("VM sample:", vm)
    rec = opt.recommend_action("cpu", 85)
    print("Recommendation:", rec)
    res = opt.apply_action(rec)
    print("Result:", res)
