<script lang="ts">
	import absencesData from '$lib/absences-data';

	const dateStrLengthWith1Day = 16;
	const formatDate = (dateStr: string) => {
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
		return new Date(`${year}-${month}-${day} ${time}`);
	};

	const getDisplayMonth = (date: Date) =>
		new Intl.DateTimeFormat('de', { month: 'long' }).formatToParts(date)[0].value;

	const daysPerWeek = 7;
	const classes = new Set<string>();
	const yearMonths: Record<string, string> = {};
	const formattedAbsencesData = absencesData.map((x) => {
		if (x.customText === 'nan') {
			x.customText = '';
		}

		const startDate = formatDate(x.startDate);
		const endDate = formatDate(x.endDate);

		classes.add(x.class);

		yearMonths[`${startDate.getUTCFullYear()}-${startDate.getUTCMonth()}`] ??=
			`${getDisplayMonth(startDate)} ${startDate.getUTCFullYear()}`;

		return {
			...x,
			startDate,
			endDate
		};
	});

	let renderKey: string | null = '';
	let selectedClass: string | null = null;
	let selectedYearMonth: string | null = Object.keys(yearMonths)[0] || null;
	let data = formattedAbsencesData;
	let firstDate: Date | null = null;
	let year: number | null = null;
	let monthIdx: number | null = null;
	let monthDayCount: number | null = null;
	let startMondayOffset: number | null = null;
	let weeks: { day: number; display: boolean }[][] = [];

	const loadDataSet = () => {
		if (data.length > 0) {
			firstDate = new Date(data[0].startDate);
			year = firstDate.getUTCFullYear();
			monthIdx = firstDate.getUTCMonth();
			monthDayCount = new Date(year, monthIdx + 1, 0).getDate();
			startMondayOffset = new Date(year!, monthIdx!).getUTCDay();

			// clear old data set
			weeks = [];

			// October 2024: 31 + 1 -> 32
			const fullWeeks = monthDayCount + startMondayOffset;
			const fillDays = Math.ceil(fullWeeks / daysPerWeek); // ceil(32 / 7) -> 5

			// October 2024: 32 + 5 - (7 - 5) -> 35 (1 for start offset, 3 for final offset)
			for (
				let i = 0;
				i < fullWeeks + fillDays - (daysPerWeek - fillDays) + startMondayOffset;
				i += 1
			) {
				const week = Math.trunc(i / daysPerWeek);
				const day = i - startMondayOffset + 1;

				weeks[week] ??= [];
				weeks[week].push({
					day,
					display: startMondayOffset <= i && day <= monthDayCount
				});
			}

			// remove empty weeks
			weeks = weeks.filter((x) => x.some((d) => d.display));
		}

		renderKey = selectedYearMonth;
	};

	$: {
		data = (
			selectedClass
				? formattedAbsencesData.filter((x) => x.class === selectedClass)
				: formattedAbsencesData
		).filter(
			(x) => `${x.startDate.getUTCFullYear()}-${x.startDate.getUTCMonth()}` === selectedYearMonth
		);

		loadDataSet();
	}

	// missing: N, O, V
	const reasonColors: Record<string, string> = {
		A: 'bg-green-500', // Attest
		P: 'bg-red-200', // Privat
		S: 'bg-red-700', // Schulische Abwesenheit
		K: 'bg-red-300' // Krank
	};
</script>

<div>
	<select class="input" bind:value={selectedClass}>
		<option value={null}>Alle Klassen</option>
		{#each classes as className}
			<option value={className}>{className}</option>
		{/each}
	</select>

	<select class="input" bind:value={selectedYearMonth}>
		{#each Object.entries(yearMonths) as [yearMonth, yearMonthDisplay]}
			<option value={yearMonth}>{yearMonthDisplay}</option>
		{/each}
	</select>
</div>

{#if data.length > 0 && firstDate && monthIdx && monthDayCount && year}
	<div class="text-xl">
		Monat: {getDisplayMonth(new Date(year, monthIdx))}
	</div>

	<div class="grid grid-flow-row text-center">
		<div class="grid grid-cols-7 grid-flow-col">
			<div>Montag</div>
			<div>Dienstag</div>
			<div>Mittwoch</div>
			<div>Donnerstag</div>
			<div>Freitag</div>
			<div>Samstag</div>
			<div>Sonntag</div>
		</div>

		{#key renderKey}
			{#each weeks as week}
				<div class="grid grid-cols-7 grid-flow-col">
					{#each week as { day, display }}
						{@const date = new Date(year, monthIdx, day)}
						{@const absences = !display
							? []
							: data.filter((x) => {
									// too early
									if (date.getMonth() < x.startDate.getMonth()) {
										return false;
									}

									// too late
									if (x.endDate.getMonth() < date.getMonth()) {
										return false;
									}

									// first or last day of absence
									if (
										date.getDate() === x.startDate.getDate() ||
										date.getDate() === x.endDate.getDate()
									) {
										return true;
									}

									// within time frame
									return x.startDate < date && date < x.endDate;
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
		{/key}
	</div>
{:else}
	<p>
		Keine Daten für die Klasse <b>{selectedClass}</b> im Zeitraum
		<b>{yearMonths[selectedYearMonth || ''] || '<NULL>'}</b>
	</p>
{/if}
