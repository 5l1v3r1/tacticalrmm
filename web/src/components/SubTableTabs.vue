<template>
    <div class="q-pa-md">
        <q-tabs
            v-model="subtab"
            dense
            inline-label
            class="text-grey"
            active-color="primary"
            indicator-color="primary"
            align="left"
            narrow-indicator
            no-caps
        >
            <q-tab name="summary" icon="fas fa-info-circle" size="xs" label="Summary" />
            <q-tab name="checks" icon="fas fa-check-double" label="Checks" />
            <q-tab name="patches" icon="system_update" label="Patches" />
            <q-tab name="software" icon="fab fa-windows" label="Software" />
        </q-tabs>
        <q-separator />
        <q-tab-panels v-model="subtab" :animated="false">
            <q-tab-panel name="summary">
                <SummaryTab />
            </q-tab-panel>
            <q-tab-panel name="checks">
                <ChecksTab />
            </q-tab-panel>
            <q-tab-panel name="patches">
                <WindowsUpdates />
            </q-tab-panel>
            <q-tab-panel name="software">
                <SoftwareTab />
            </q-tab-panel>
        </q-tab-panels>
    </div>
</template>

<script>
import SummaryTab from '@/components/SummaryTab';
import ChecksTab from '@/components/ChecksTab';
import WindowsUpdates from '@/components/WindowsUpdates';
import SoftwareTab from '@/components/SoftwareTab';
export default {
  name: "SubTableTabs",
  components: {
      SummaryTab,
      ChecksTab,
      WindowsUpdates,
      SoftwareTab,
  },
  data() {
      return {
          subtab: 'summary'
      }
  }
};
</script>

