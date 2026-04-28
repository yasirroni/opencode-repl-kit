function result = filterData(data, column, value, operator)
    % filterData - Filter data by a condition on a column.
    %
    % Args:
    %   data: Numeric array or struct array.
    %   column: Field name (for struct data) or ignored (for numeric data).
    %   value: Value to compare against.
    %   operator: One of '==', '~=', '>', '<', '>=', '<='.
    %
    % Returns:
    %   Filtered array (same type as input).

    if isempty(data)
        result = data;
        return;
    end

    if isstruct(data)
        values = [data.(column)];
    else
        values = data;
    end

    mask = apply_comparison(values, value, operator);

    if isstruct(data)
        result = data(mask);
    else
        result = data(mask);
    end
end

function mask = apply_comparison(values, value, operator)
    switch operator
        case '=='
            mask = values == value;
        case '~='
            mask = values ~= value;
        case '>'
            mask = ~isnan(values) & (values > value);
        case '<'
            mask = ~isnan(values) & (values < value);
        case '>='
            mask = ~isnan(values) & (values >= value);
        case '<='
            mask = ~isnan(values) & (values <= value);
        otherwise
            error('Unknown operator: %s', operator);
    end
end
