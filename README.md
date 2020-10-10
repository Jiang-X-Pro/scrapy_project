# scrapy_project
something interesting
  int a = (0x55) | (0x55 << 8);
  int mask0 = a | (a << 16);
  int b = (0x33) | (0x33 << 8);
  int mask1 = b | (b << 16);
  int c = (0x0F) | (0x0F << 8);
  int mask2 = c | (c << 16);
  int mask3 = (0xFF) | (0xFF << 16);
  int mask4 = (0xFF) | (0xFF << 8);

  //unsigned int n = (unsigned int)x;
  int n = x;
  n = (n & mask0) + (n >> 0x01  & mask0);
  n = (n & mask1) + (n >> 0x02  & mask1);
  n = (n & mask2) + (n >> 0x04  & mask2);
  n = (n & mask3) + (n >> 0x08  & mask3);
  n = (n & mask4) + (n >> 0x10  & mask4);

  return n;
