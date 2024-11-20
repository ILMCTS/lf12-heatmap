<script lang="ts">
	import absencesData from '$lib/absences-data';

	const dateStrLengthWith1Day = 16;
	const formatDate = (dateStr: string): string => {
		// shameless
		// 8102024 17:00:00 -> 08102024 17:00:00
		if (dateStr.length === dateStrLengthWith1Day) {
			dateStr = dateStr.padStart(dateStrLengthWith1Day + 1, '0');
		}

		// Extract the day, month, year, and time from the input string
		const day = dateStr.slice(0, 2);
		const month = dateStr.slice(2, 4);
		const year = dateStr.slice(4, 8);
		const time = dateStr.slice(9); // Extract time part after space

		// Format the date as YYYY-MM-DD and combine with time
		return `${year}-${month}-${day} ${time}`;
	};

	const classes = new Set<string>();
	const formattedAbsencesData = absencesData.map((x) => {
		if (x.customText === 'nan') {
			x.customText = '';
		}

		x.startDate = formatDate(x.startDate);
		x.endDate = formatDate(x.endDate);

		classes.add(x.class);

		return x;
	});

	let selectedClass: string | null = null;
	let data = formattedAbsencesData;
	let firstDate: Date | null = null;
	let lastDate: Date | null = null;
	let year: number | null = null;
	let monthIdx: number | null = null;
	let monthDayCount: number | null = null;
	let startMondayOffset: number | null = null;
	let weeks: { day: number; display: boolean }[][] = [];

	const loadDataSet = () => {
		if (data.length > 0) {
			firstDate = new Date(data[0].startDate);
			lastDate = new Date(data[data.length - 1].endDate);
			year = firstDate.getFullYear();
			monthIdx = firstDate.getMonth();
			monthDayCount = new Date(year, monthIdx + 1, 0).getDate();
			startMondayOffset = 1;

			// clear old data set
			weeks = [];

			// October 2024: 31 + 1 -> 32
			const fullWeeks = monthDayCount + startMondayOffset;
			const fillDays = Math.ceil(fullWeeks / daysPerWeek); // ceil(32 / 7) -> 5

			// October 2024: 32 + 5 - (7 - 5) -> 35 (1 for start offset, 3 for final offset)
			for (let i = 0; i < fullWeeks + fillDays - (daysPerWeek - fillDays); i += 1) {
				const week = Math.trunc(i / daysPerWeek);
				const day = i - startMondayOffset + 1;

				weeks[week] ??= [];
				weeks[week].push({
					day,
					display: !(i < startMondayOffset || monthDayCount < i)
				});
			}
		}
	};

	$: {
		data = selectedClass
			? formattedAbsencesData.filter((x) => x.class === selectedClass)
			: formattedAbsencesData;

		loadDataSet();

		console.log(classes);
	}

	const daysPerWeek = 7;

	// missing: N, O, V
	const reasonColors: Record<string, string> = {
		A: 'bg-green-500', // Attest
		P: 'bg-red-200', // Privat
		S: 'bg-red-700', // Schulische Abwesenheit
		K: 'bg-red-300' // Krank
	};
</script>

<select bind:value={selectedClass}>
	{#each classes as className}
		<option value={className}>{className}</option>
	{/each}
</select>

{#if firstDate && lastDate && monthIdx && monthDayCount && year}
	<div class="text-xl">
		Monat: {new Intl.DateTimeFormat('de', { month: 'long' }).formatToParts(
			new Date(year, monthIdx)
		)[0].value}
	</div>

	<div class="grid grid-flow-row text-center">
		<div class="grid grid-flow-col">
			<div>Montag</div>
			<div>Dienstag</div>
			<div>Mittwoch</div>
			<div>Donnerstag</div>
			<div>Freitag</div>
			<div>Samstag</div>
			<div>Sonntag</div>
		</div>

		{#each weeks as week}
			<div class="grid grid-cols-7 grid-flow-col">
				{#each week as { day, display }}
					{@const date = new Date(year, monthIdx, day)}
					{@const absences = !display
						? []
						: data.filter((x) => {
								const startDate = new Date(x.startDate);
								const endDate = new Date(x.endDate);

								// too early
								if (date.getMonth() < startDate.getMonth()) {
									return false;
								}

								// too late
								if (endDate.getMonth() < date.getMonth()) {
									return false;
								}

								// first or last day of absence
								if (
									date.getDate() === startDate.getDate() ||
									date.getDate() === endDate.getDate()
								) {
									return true;
								}

								// within time frame
								return startDate < date && date < endDate;
							})}
					{@const red = 50}
					{@const green = 30 + 20 * absences.length}
					{@const blue = 50}

					<div
						class="p-2"
						style="background-color: rgb({red}, {green}, {blue})"
						title="{absences.length} absences"
					>
						{#if display}
							{day}
						{/if}
					</div>
				{/each}
			</div>
		{/each}
	</div>
{/if}
