// MIT License

// Copyright (c) 2024 Litrin Jiang

// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:

// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.

// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

#include <stdio.h>
#include <unistd.h>

#define ENABLE '1'
#define DISABLE '0'

const char CPU_PATH[37]={"/sys/devices/system/cpu/cpu%d/online"};

void usage()
{
	printf("Usage:\n");
	printf("enable_core [-e|-d] <coreset string> enable|disable cores \n");

	printf("e.g., disable_cpu -e 1,3-5 \n");
}

int set_state(int core, char state)
{
	if (core < 0) return 0;
	char file_path[38];
	sprintf(file_path, CPU_PATH, core);


	FILE* fd;
	fd = fopen(file_path, "w");
	if (fd == NULL)
	{
		printf("Core #%d is not exist!\n", core);
		return 1;
	}

	fputs(&state, fd);

	fclose(fd);
	return 0;
}

int coreset_from_char(char *s, char state)
{
	int cur = 0;
	int tmp = -1;
	int err = 0;

  for (int i=0; s[i] != '\0'; ++i)
	{
		if (s[i] == ',')
		{
			tmp = tmp < 0 ? cur : tmp ;
			for(int i = tmp; i<= cur; i++)
				err += set_state(i, state);
      
 			tmp = -1;
			cur = 0;
			continue;
		}

		if (s[i] == '-')
		{
			tmp = cur;
			cur = 0;
			continue;
		}
		cur = cur * 10 + (int)s[i] - 48;
	}

	tmp = tmp < 0 ? cur : tmp;
	for(int i = tmp; i <= cur; i++)
		err += set_state(i, state);

  return err;

}

int main(int argc, char *argv[])
{
	if (argc == 1)
	{
		usage();
		return 0;
	}

	int option;
	while ((option = getopt(argc, argv, "e:d:")) != -1)
	{
		switch (option)
		{
			case 'e':
				return coreset_from_char(optarg, ENABLE);

			case 'd':
				return coreset_from_char(optarg, DISABLE);

			case '?':
				usage();
				return 0; 
		}
	}
}
