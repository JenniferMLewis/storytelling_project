
# Swarm plot of Categorical Columns [This prepares processing death for this dataframe, but might be interesting for smaller data sets]

# def cat_swarm(train, quant, target):
#   '''
#   Takes in a TRAIN Dataframe, quantative value column, and target; returns a swarmplot of Categorical data vs entered quantative value column, target dictates hue.
#   Uses the Acquire sheet function 'dtypes_to_list' to pull out Categorical column names.
#   '''
#   num_type, cat_type = dtypes_to_list(train)
#   for col in train.columns:
#       if col in cat_type:
#         sns.swarmplot(x=col, y=quant, data=train, hue=target)
#         plt.show()

