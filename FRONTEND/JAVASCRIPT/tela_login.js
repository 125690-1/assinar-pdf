function formatarBR(input) {
  const prefixo = 'BR0';
  const numeros = input.value.replace(/\D/g, '').substring(1); // remove o B, R e mantém só os números
  input.value = prefixo + numeros.slice(0, 9); // total de 12 caracteres
}
