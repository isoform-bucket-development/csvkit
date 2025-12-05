/**
 * Unit tests for Tetromino shapes
 * Tests all seven standard tetromino shapes per REQ-2
 */

const {
  Tetromino,
  createTetromino,
  generateRandomTetromino,
  TETROMINO_TYPES,
  TETROMINO_COLORS,
  TETROMINO_SHAPES
} = require('../src/tetromino.js');

describe('Tetromino Shapes Generation', () => {

  describe('Test Case 1: Generate I-piece', () => {
    test('I-piece has 4 cells in horizontal line', () => {
      const iPiece = createTetromino('I');
      const cells = iPiece.getCells();

      // Should have exactly 4 cells
      expect(cells.length).toBe(4);

      // All cells should be in same row (horizontal line)
      const rows = cells.map(cell => cell[0]);
      const uniqueRows = [...new Set(rows)];
      expect(uniqueRows.length).toBe(1);

      // Columns should span 4 consecutive positions
      const cols = cells.map(cell => cell[1]).sort((a, b) => a - b);
      expect(cols).toEqual([0, 1, 2, 3]);
    });

    test('I-piece has cyan color', () => {
      const iPiece = createTetromino('I');
      expect(iPiece.getColor()).toBe('cyan');
    });

    test('I-piece has correct type', () => {
      const iPiece = createTetromino('I');
      expect(iPiece.getType()).toBe('I');
    });
  });

  describe('Test Case 2: Generate O-piece', () => {
    test('O-piece has 2x2 square shape', () => {
      const oPiece = createTetromino('O');
      const cells = oPiece.getCells();

      // Should have exactly 4 cells
      expect(cells.length).toBe(4);

      // Should have 2 unique rows and 2 unique columns
      const rows = cells.map(cell => cell[0]);
      const cols = cells.map(cell => cell[1]);
      const uniqueRows = [...new Set(rows)];
      const uniqueCols = [...new Set(cols)];
      expect(uniqueRows.length).toBe(2);
      expect(uniqueCols.length).toBe(2);

      // Bounding box should be 2x2
      const boundingBox = oPiece.getBoundingBox();
      expect(boundingBox.width).toBe(2);
      expect(boundingBox.height).toBe(2);
    });

    test('O-piece has yellow color', () => {
      const oPiece = createTetromino('O');
      expect(oPiece.getColor()).toBe('yellow');
    });

    test('O-piece has correct type', () => {
      const oPiece = createTetromino('O');
      expect(oPiece.getType()).toBe('O');
    });
  });

  describe('Test Case 3: Generate T-piece', () => {
    test('T-piece has T-shaped pattern with 4 cells', () => {
      const tPiece = createTetromino('T');
      const cells = tPiece.getCells();

      // Should have exactly 4 cells
      expect(cells.length).toBe(4);

      // T-shape: 3 cells in top row, 1 cell below middle
      // ███
      //  █
      const topRow = cells.filter(cell => cell[0] === 0);
      const bottomRow = cells.filter(cell => cell[0] === 1);
      expect(topRow.length).toBe(3);
      expect(bottomRow.length).toBe(1);

      // Bottom cell should be in the middle column
      expect(bottomRow[0][1]).toBe(1);
    });

    test('T-piece has purple color', () => {
      const tPiece = createTetromino('T');
      expect(tPiece.getColor()).toBe('purple');
    });

    test('T-piece has correct type', () => {
      const tPiece = createTetromino('T');
      expect(tPiece.getType()).toBe('T');
    });
  });

  describe('Test Case 4: Generate S-piece', () => {
    test('S-piece has S-shaped zigzag pattern', () => {
      const sPiece = createTetromino('S');
      const cells = sPiece.getCells();

      // Should have exactly 4 cells
      expect(cells.length).toBe(4);

      // S-shape: 2 cells in top row (right side), 2 cells in bottom row (left side)
      //  ██
      // ██
      const topRow = cells.filter(cell => cell[0] === 0);
      const bottomRow = cells.filter(cell => cell[0] === 1);
      expect(topRow.length).toBe(2);
      expect(bottomRow.length).toBe(2);

      // Top row should be shifted right compared to bottom row
      const topCols = topRow.map(cell => cell[1]).sort((a, b) => a - b);
      const bottomCols = bottomRow.map(cell => cell[1]).sort((a, b) => a - b);
      expect(topCols[0]).toBeGreaterThan(bottomCols[0]);
    });

    test('S-piece has green color', () => {
      const sPiece = createTetromino('S');
      expect(sPiece.getColor()).toBe('green');
    });

    test('S-piece has correct type', () => {
      const sPiece = createTetromino('S');
      expect(sPiece.getType()).toBe('S');
    });
  });

  describe('Test Case 5: Generate Z-piece', () => {
    test('Z-piece has Z-shaped zigzag pattern', () => {
      const zPiece = createTetromino('Z');
      const cells = zPiece.getCells();

      // Should have exactly 4 cells
      expect(cells.length).toBe(4);

      // Z-shape: 2 cells in top row (left side), 2 cells in bottom row (right side)
      // ██
      //  ██
      const topRow = cells.filter(cell => cell[0] === 0);
      const bottomRow = cells.filter(cell => cell[0] === 1);
      expect(topRow.length).toBe(2);
      expect(bottomRow.length).toBe(2);

      // Top row should be shifted left compared to bottom row
      const topCols = topRow.map(cell => cell[1]).sort((a, b) => a - b);
      const bottomCols = bottomRow.map(cell => cell[1]).sort((a, b) => a - b);
      expect(topCols[0]).toBeLessThan(bottomCols[1]);
      expect(topCols[1]).toBe(bottomCols[0]); // Overlap in middle
    });

    test('Z-piece has red color', () => {
      const zPiece = createTetromino('Z');
      expect(zPiece.getColor()).toBe('red');
    });

    test('Z-piece has correct type', () => {
      const zPiece = createTetromino('Z');
      expect(zPiece.getType()).toBe('Z');
    });
  });

  describe('Test Case 6: Generate J-piece', () => {
    test('J-piece has J-shaped pattern with 4 cells', () => {
      const jPiece = createTetromino('J');
      const cells = jPiece.getCells();

      // Should have exactly 4 cells
      expect(cells.length).toBe(4);

      // J-shape: 1 cell in top row (left), 3 cells in bottom row
      // █
      // ███
      const topRow = cells.filter(cell => cell[0] === 0);
      const bottomRow = cells.filter(cell => cell[0] === 1);
      expect(topRow.length).toBe(1);
      expect(bottomRow.length).toBe(3);

      // Top cell should be in leftmost column of bottom row
      const bottomCols = bottomRow.map(cell => cell[1]).sort((a, b) => a - b);
      expect(topRow[0][1]).toBe(bottomCols[0]);
    });

    test('J-piece has blue color', () => {
      const jPiece = createTetromino('J');
      expect(jPiece.getColor()).toBe('blue');
    });

    test('J-piece has correct type', () => {
      const jPiece = createTetromino('J');
      expect(jPiece.getType()).toBe('J');
    });
  });

  describe('Test Case 7: Generate L-piece', () => {
    test('L-piece has L-shaped pattern with 4 cells', () => {
      const lPiece = createTetromino('L');
      const cells = lPiece.getCells();

      // Should have exactly 4 cells
      expect(cells.length).toBe(4);

      // L-shape: 1 cell in top row (right), 3 cells in bottom row
      //   █
      // ███
      const topRow = cells.filter(cell => cell[0] === 0);
      const bottomRow = cells.filter(cell => cell[0] === 1);
      expect(topRow.length).toBe(1);
      expect(bottomRow.length).toBe(3);

      // Top cell should be in rightmost column of bottom row
      const bottomCols = bottomRow.map(cell => cell[1]).sort((a, b) => a - b);
      expect(topRow[0][1]).toBe(bottomCols[bottomCols.length - 1]);
    });

    test('L-piece has orange color', () => {
      const lPiece = createTetromino('L');
      expect(lPiece.getColor()).toBe('orange');
    });

    test('L-piece has correct type', () => {
      const lPiece = createTetromino('L');
      expect(lPiece.getType()).toBe('L');
    });
  });

  describe('All tetromino types are defined', () => {
    test('All seven standard shapes are available', () => {
      expect(TETROMINO_TYPES).toContain('I');
      expect(TETROMINO_TYPES).toContain('O');
      expect(TETROMINO_TYPES).toContain('T');
      expect(TETROMINO_TYPES).toContain('S');
      expect(TETROMINO_TYPES).toContain('Z');
      expect(TETROMINO_TYPES).toContain('J');
      expect(TETROMINO_TYPES).toContain('L');
      expect(TETROMINO_TYPES.length).toBe(7);
    });

    test('All shapes have correct color assignments', () => {
      expect(TETROMINO_COLORS.I).toBe('cyan');
      expect(TETROMINO_COLORS.O).toBe('yellow');
      expect(TETROMINO_COLORS.T).toBe('purple');
      expect(TETROMINO_COLORS.S).toBe('green');
      expect(TETROMINO_COLORS.Z).toBe('red');
      expect(TETROMINO_COLORS.J).toBe('blue');
      expect(TETROMINO_COLORS.L).toBe('orange');
    });

    test('All shapes have exactly 4 cells', () => {
      TETROMINO_TYPES.forEach(type => {
        const shape = TETROMINO_SHAPES[type];
        expect(shape.length).toBe(4);
      });
    });
  });

  describe('Tetromino class functionality', () => {
    test('createTetromino factory function works', () => {
      const tetromino = createTetromino('T');
      expect(tetromino).toBeInstanceOf(Tetromino);
    });

    test('getCellCount returns correct count', () => {
      TETROMINO_TYPES.forEach(type => {
        const tetromino = createTetromino(type);
        expect(tetromino.getCellCount()).toBe(4);
      });
    });

    test('Invalid type throws error', () => {
      expect(() => createTetromino('X')).toThrow('Invalid tetromino type: X');
    });

    test('generateRandomTetromino returns valid tetromino', () => {
      const tetromino = generateRandomTetromino();
      expect(tetromino).toBeInstanceOf(Tetromino);
      expect(TETROMINO_TYPES).toContain(tetromino.getType());
    });
  });
});
