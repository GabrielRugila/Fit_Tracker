import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import plotly.express as px

# --------------------------------------------------------------
# Load data
# --------------------------------------------------------------
df = pd.read_pickle("../../data/interim/01data_resampled.pkl")

# --------------------------------------------------------------
# Plot single columns
# --------------------------------------------------------------
set_ddf = df[df["set"] == 1]
plt.plot(set_ddf["acc_y"].reset_index(drop=True))

# --------------------------------------------------------------
# Plot all exercises
# --------------------------------------------------------------
for label in df['label'].unique():
  subset = df[df['label'] == label]
  # display(subset.head())
  fig, ax = plt.subplots()
  plt.plot(subset["acc_y"].reset_index(drop=True), label=label)
  plt.legend()
  plt.show()

for label in df['label'].unique():
  subset = df[df['label'] == label]
  # display(subset.head())
  fig, ax = plt.subplots()
  plt.plot(subset[:100]["acc_y"].reset_index(drop=True), label=label)
  plt.legend()
  plt.show()
# --------------------------------------------------------------
# Adjust plot settings
# --------------------------------------------------------------
mpl.style.use("seaborn-v0_8-deep")
mpl.rcParams['figure.figsize'] = (20, 5)
mpl.rcParams['figure.dpi'] = 100

# --------------------------------------------------------------
# Compare medium vs. heavy sets
# --------------------------------------------------------------
category_df = df.query("label == 'squat'").query("participant == 'A'").reset_index()

fig, ax = plt.subplots()
# category_df.groupby(["category"])["acc_y"].plot()
df.query("label == 'squat'").query("participant == 'A'").query("category == 'heavy'").reset_index()["acc_y"].plot(ax=ax, label="heavy", alpha=0.7)
df.query("label == 'squat'").query("participant == 'A'").query("category == 'medium'").reset_index()["acc_y"].plot(ax=ax, label="medium", alpha=0.7)
ax.set_ylabel("acc_y")
ax.set_xlabel("samples")
plt.legend()
plt.show()

# --------------------------------------------------------------
# Compare participants
# --------------------------------------------------------------
participant_df = df.query("label == 'bench'").sort_values(['participant', 'set']).reset_index()

fig, ax = plt.subplots()
participant_df.groupby("participant")["acc_y"].plot()
ax.set_ylabel("acc_y")
ax.set_xlabel("set")
plt.legend()
plt.show()

# --------------------------------------------------------------
# Plot multiple axis
# --------------------------------------------------------------
label = "squat"
participant = "A"
all_ax_df = df.query(f"label == '{label}'").query(f"participant == '{participant}'").reset_index()

fig, ax = plt.subplots()
all_ax_df[['acc_x', 'acc_y', 'acc_z']].plot(ax=ax)
ax.set_ylabel("acc")
ax.set_xlabel("samples")
plt.legend()
plt.show()

# --------------------------------------------------------------
# Create a loop to plot all combinations per sensor
# --------------------------------------------------------------
labels = df['label'].unique()
participants = df['participant'].unique()

for label in labels:
  for participant in participants:
    all_ax_df = df.query(f"label == '{label}'").query(f"participant == '{participant}'").sort_values(['participant', 'set']).reset_index()

    if len(all_ax_df) > 0:
      
      fig, ax = plt.subplots()
      all_ax_df[['acc_x', 'acc_y', 'acc_z']].plot(ax=ax)
      ax.set_ylabel("acc")
      ax.set_xlabel("samples")
      plt.title(f"{label} - {participant}".title())
      plt.legend()
      plt.show()

for label in labels:
  for participant in participants:
    all_ax_df = df.query(f"label == '{label}'").query(f"participant == '{participant}'").sort_values(['participant', 'set']).reset_index()

    if len(all_ax_df) > 0:
      
      fig, ax = plt.subplots()
      all_ax_df[['gyr_x', 'gyr_y', 'gyr_z']].plot(ax=ax)
      ax.set_ylabel("gyr")
      ax.set_xlabel("samples")
      plt.title(f"{label} - {participant}".title())
      plt.legend()
      plt.show()

# --------------------------------------------------------------
# Combine plots in one figure
# --------------------------------------------------------------
label = "row"
participant = "A"
combined_plot_df = (
  df.query(f"label == '{label}'")
  .query(f"participant == '{participant}'")
  .sort_values(['participant', 'set'])
  .reset_index(drop=True)
)

fig, ax = plt.subplots(2, 1, sharex=True, figsize=(20, 10))
combined_plot_df[['acc_x', 'acc_y', 'acc_z']].plot(ax=ax[0])
combined_plot_df[['gyr_x', 'gyr_y', 'gyr_z']].plot(ax=ax[1])

ax[0].legend(loc="upper center", bbox_to_anchor=(0.5, 1.05), ncol=3, fancybox=True, shadow=True)
ax[1].legend(loc="upper center", bbox_to_anchor=(0.5, 1.05), ncol=3, fancybox=True, shadow=True)
ax[1].set_xlabel("samples")

plt.suptitle(f"{label} - {participant}".title())
plt.show()

# --------------------------------------------------------------
# Loop over all combinations and export for both sensors
# --------------------------------------------------------------
labels = df['label'].unique()
participants = df['participant'].unique()

for label in labels:
  for participant in participants:
    combined_plot_df = df.query(f"label == '{label}'").query(f"participant == '{participant}'").sort_values(['participant', 'set']).reset_index()

    if len(combined_plot_df) > 0:
        
        fig, ax = plt.subplots(2, 1, sharex=True, figsize=(20, 10))
        combined_plot_df[['acc_x', 'acc_y', 'acc_z']].plot(ax=ax[0])
        combined_plot_df[['gyr_x', 'gyr_y', 'gyr_z']].plot(ax=ax[1])
  
        ax[0].legend(loc="upper center", bbox_to_anchor=(0.5, 1.05), ncol=3, fancybox=True, shadow=True)
        ax[1].legend(loc="upper center", bbox_to_anchor=(0.5, 1.05), ncol=3, fancybox=True, shadow=True)
        ax[1].set_xlabel("samples")
  
        plt.suptitle(f"{label} - {participant}".title())

        plt.show()

        plt.savefig(f"../../reports/figures/02visualization/{label}_{participant}.png")
        plt.close()