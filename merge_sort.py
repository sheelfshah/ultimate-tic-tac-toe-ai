# Python program for implementation of MergeSort 

# Merges two subarrays of arr[]. 
# First subarray is arr[l..m] 
# Second subarray is arr[m+1..r] 
# arr has scores, grid_indices has indices
def merge(arr, grid_indices, l, m, r): 
	n1 = m - l + 1
	n2 = r- m 
	L = [0] * (n1) 
	R = [0] * (n2) 
	LG = [0] * (n1) 
	RG = [0] * (n2) 
	for i in range(0 , n1): 
		L[i] = arr[l + i] 
		LG[i]=grid_indices[l+i]
	for j in range(0 , n2): 
		R[j] = arr[m + 1 + j] 
		RG[j]=grid_indices[m+1+j]

	i = 0	 # Initial index of first subarray 
	j = 0	 # Initial index of second subarray 
	k = l	 # Initial index of merged subarray 

	while i < n1 and j < n2 : 
		if L[i] <= R[j]: 
			arr[k] = L[i]
			grid_indices[k]=LG[i]
			i += 1
		else: 
			arr[k] = R[j]
			grid_indices[k]=RG[j] 
			j += 1
		k += 1

	# Copy the remaining elements of L[], if any
	while i < n1: 
		arr[k] = L[i] 
		grid_indices[k]=LG[i]
		i += 1
		k += 1

	# Copy the remaining elements of R[], if any 
	while j < n2: 
		arr[k] = R[j]
		grid_indices[k]=RG[j] 
		j += 1
		k += 1

# l is for left index and r is right index of the 
# sub-array of arr to be sorted 
def mergeSort(arr, grid_indices,l,r): 
	if l < r: 

		# Same as (l+r)//2, but avoids overflow for 
		# large l and h 
		m = (l+(r-1))//2

		# Sort first and second halves 
		mergeSort(arr, grid_indices, l, m) 
		mergeSort(arr, grid_indices, m+1, r) 
		merge(arr, grid_indices, l, m, r) 
		return grid_indices