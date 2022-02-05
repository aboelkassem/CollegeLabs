// See https://aka.ms/new-console-template for more information
Console.WriteLine("CS431 Parallel Computation Task");

var size_of_rows = 20;
var size_of_columns = 30;

var matrixX = new int[size_of_rows, size_of_columns]; 
var matrixY = new int[size_of_rows, size_of_columns]; 
var matrixZ = new int[size_of_rows, size_of_columns]; 
var matrixW = new int[size_of_rows, size_of_columns];

var randNum = new Random();
var watch = new System.Diagnostics.Stopwatch();

// fill the matrices with random numbers 
for (int i = 0; i < size_of_rows; i++)
    for (int j = 0; j < size_of_columns; j++)
    {
        matrixX[i, j] = randNum.Next(1, 100000);
        matrixY[i, j] = randNum.Next(1, 100000);
        matrixZ[i, j] = randNum.Next(1, 100000);
        matrixW[i, j] = randNum.Next(1, 100000);
    }

watch.Start();
SequentialProcess(matrixX, matrixY, matrixZ, matrixW, size_of_rows , size_of_columns);
watch.Stop();
Console.WriteLine();
Console.WriteLine("========================================================");
Console.WriteLine($"Sequencial process execution time: {watch.ElapsedMilliseconds} ms");
Console.WriteLine("========================================================");

var watch2 = new System.Diagnostics.Stopwatch();
watch2.Start();
await ParallelProcess(matrixX, matrixY, matrixZ, matrixW, size_of_rows, size_of_columns);
watch2.Stop();
Console.WriteLine();
Console.WriteLine("========================================================");
Console.WriteLine($"Parallel process execution time: {watch2.ElapsedMilliseconds} ms");
Console.WriteLine("========================================================");

void SequentialProcess(int[,] x , int[,] y, int[,] z, int[,] w , int rows_size , int columns_size)
{
    int [,] f1 = new int[rows_size, columns_size];
    int [,] f2 = new int[rows_size, columns_size];
    int [,] result = new int[rows_size, columns_size];

    // sum of x + y
    f1 = Sum(x, y, rows_size , columns_size);

    // sum of z + w
    f2 = Sum(z, w, rows_size, columns_size);

    // multiplication f1 * f2
    result = Multiple(f1, f2, rows_size, columns_size);

    // print result
    Console.WriteLine("The result matrix of sequential process");
    Print(result, rows_size, columns_size);
}

async Task ParallelProcess(int[,] x, int[,] y, int[,] z, int[,] w, int rows_size, int columns_size)
{
    int[,] f1 = new int[rows_size, columns_size];
    int[,] f2 = new int[rows_size, columns_size];
    int[,] result = new int[rows_size, columns_size];

    // sum of x + y
    f1 = await SumAsync(x, y, rows_size , columns_size);

    // sum of z + w
    f2 = await SumAsync(z, w, rows_size, columns_size);

    // multiplication f1 * f2
    result = await MultipleAsync(f1, f2, rows_size, columns_size);

    // print result
    Console.WriteLine("The result matrix of sequential process");
    await PrintAsync(result, rows_size, columns_size);

    //// Another approach
    //var sumTask = SumAsync(x, y, size);
    //var secondSumTask = SumAsync(z, w, size);
    //var multipliTask = MultipleAsync(f1, f2, size);

    //Console.WriteLine("The result matrix of sequential process");
    //var printTask = PrintAsync(result, size);

    //// execute all task at the same time
    //await Task.WhenAll(sumTask, secondSumTask, multipliTask, printTask);
}

int[,] Sum(int[,] x, int [,] y, int rows_size, int columns_size)
{
    var result = new int[rows_size, columns_size];
    for (int i = 0; i < rows_size; i++)
        for (int j = 0; j < columns_size; j++)
            result[i, j] = x[i, j] + y[i, j];

    return result;
}

async Task<int[,]> SumAsync(int[,] x, int[,] y, int rows_size, int columns_size)
{
    var result = new int[rows_size, columns_size];
    await Task.Run(() =>
    {
        for (int i = 0; i < rows_size; i++)
            for (int j = 0; j < columns_size; j++)
                result[i, j] = x[i, j] + y[i, j];
    });

    return result;
}

int[,] Multiple(int[,] x, int[,] y, int rows_size, int columns_size)
{
    var result = new int[rows_size, columns_size];
    for (int i = 0; i < rows_size; i++)
        for (int j = 0; j < columns_size; j++)
            result[i, j] = x[i, j] * y[i, j];

    return result;
}

async Task<int[,]> MultipleAsync(int[,] x, int[,] y, int rows_size, int columns_size)
{
    var result = new int[rows_size, columns_size];
    await Task.Run(() =>
    {
        for (int i = 0; i < rows_size; i++)
            for (int j = 0; j < columns_size; j++)
                result[i, j] = x[i, j] * y[i, j];
    });

    return result;
}

void Print(int[,] array, int rows_size, int columns_size)
{
    for (int i = 0; i < rows_size; i++)
    {
        for (int j = 0; j < columns_size; j++)
            Console.Write($"{array[i, j]} ");
        Console.WriteLine();
    }
}

async Task PrintAsync(int[,] array, int rows_size, int columns_size)
{
    await Task.Run(() =>
    {
        for (int i = 0; i < rows_size; i++)
        {
            for (int j = 0; j < columns_size; j++)
                Console.Write($"{array[i, j]} ");
            Console.WriteLine();
        }
    });
}